#!/usr/bin/env python3
import os, re, sys, subprocess

# ----------------- 유틸 함수 -----------------
def is_executable(full_path):
    """Wine, Flatpak, 심볼릭 링크 포함 실행 가능 판별"""
    try:
        if not os.path.exists(full_path):
            return False
        if os.path.isfile(full_path) and os.access(full_path, os.X_OK):
            return True
        if os.path.islink(full_path):
            target = os.path.realpath(full_path)
            if os.access(target, os.X_OK):
                return True
        if full_path.startswith("/var/lib/flatpak/exports/bin/"):
            return True
        if full_path.startswith(os.path.expanduser("~/.local/share/flatpak/exports/bin/")):
            return True
        if full_path.endswith(".exe") and "/.wine/" in full_path:
            return True
    except OSError:
        return False
    return False

def parse_desktop_file(file_path):
    """.desktop 파일에서 Name, Exec, Icon, Comment 정보 추출"""
    info = {"file": file_path}
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = f.read()
        for key in ["Name", "Exec", "Icon", "Comment"]:
            match = re.search(rf"^{key}=(.+)$", data, re.MULTILINE)
            if match:
                info[key] = match.group(1)
    except Exception:
        pass
    return info

def output_result(result_list, output_type="all", outputfile_name="output.txt"):
    do_print = output_type in ("print", "all")
    do_file = output_type in ("file", "all")
    if do_print:
        print("\n".join(result_list))
    if do_file:
        with open(outputfile_name, "a", encoding="utf-8") as f:
            f.write("\n".join(result_list) + "\n")

# ----------------- 파일 시스템 검색 -----------------
def find_similar_programs(target_name, roots=None, include_all=False, include_similar_file=True):
    """디렉터리 내 target_name을 포함하는 파일 검색"""
    if roots is None:
        roots = os.environ["PATH"].split(":")
    elif isinstance(roots, str):
        roots = [roots]

    matched = []
    for directory in roots:
        if not os.path.isdir(directory):
            continue
        for current_root, _, files in os.walk(directory):
            try:
                for file_name in files:
                    pattern = re.compile(f"{re.escape(target_name)}" if include_similar_file else f"^{re.escape(target_name)}$", re.IGNORECASE)
                    if pattern.match(file_name):
                        full_path = os.path.join(current_root, file_name)
                        if include_all or is_executable(full_path):
                            matched.append(full_path)
            except (PermissionError, OSError):
                continue
    return matched

# ----------------- which/find 검색 -----------------
def fine_with_which(target_name, use_find=False):
    if use_find:
        proc = subprocess.run(['find', '/', '-name', target_name], stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, text=True)
    else:
        proc = subprocess.run(['which', target_name], capture_output=True, text=True)
    return proc.stdout.strip().split('\n')

# ----------------- 앱 목록 검색 -----------------
def find_desktop_entries(target_name):
    matched = []
    desktop_paths = ["/usr/share/applications", os.path.expanduser("~/.local/share/applications")]
    for path in desktop_paths:
        if not os.path.exists(path):
            continue
        for file in os.listdir(path):
            if not file.endswith(".desktop"):
                continue
            full_path = os.path.join(path, file)
            try:
                with open(full_path, "r", encoding="utf-8") as f:
                    content = f.read()
                if target_name.lower() in content.lower():
                    matched.append(full_path)
            except Exception:
                continue
    return matched

# ----------------- 검색 함수 -----------------
def search_filesystem(name, roots=None, include_all=False, include_similar_file=True):
    result = ["\n============= 경로로 찾음 ============="]
    found = find_similar_programs(name, roots, include_all, include_similar_file)
    result.extend(found or ["No matching files found."])
    return result, found

def search_command(name, use_find=False):
    result = ["\n============= 명령어 검색 ============="]
    found = fine_with_which(name, use_find)
    result.extend(found or ["No matching commands found."])
    return result, found

def search_desktop(name):
    result = ["\n===============  앱 목록에서 찾음  ==============="]
    desktop_files = find_desktop_entries(name)
    if desktop_files:
        for f in desktop_files:
            info = parse_desktop_file(f)
            line = f"{info.get('Name','(이름없음)')} → {info.get('Exec','(실행경로없음)')}"
            result.append(line)
            result.append(f"  파일: {f}")
            if 'Icon' in info:
                result.append(f"  아이콘: {info['Icon']}")
            if 'Comment' in info:
                result.append(f"  설명: {info['Comment']}")
            result.append("")
    else:
        result.append("No matching desktop entries found.")
    return result, desktop_files

# ----------------- 통합 실행 -----------------
def search_program(name, methods=["filesystem","command","desktop"], roots=None,
                   include_all=False, include_similar_file=True,
                   output_type="all", outputfile_name="output.txt"):

    if "filesystem" in methods:
        res, _ = search_filesystem(name, roots, include_all, include_similar_file)
        output_result(res, output_type, outputfile_name)

    if "command" in methods:
        res, _ = search_command(name, include_all)
        output_result(res, output_type, outputfile_name)

    if "desktop" in methods:
        res, _ = search_desktop(name)
        output_result(res, output_type, outputfile_name)

# ----------------- 실행 예시 -----------------
if __name__ == "__main__":
    name = input("🔍 패키지/프로그램 이름을 입력하세요: ").strip()
    methods_input = input("검색 방식 선택 (filesystem/command/desktop, 콤마로 구분) [기본: 모두]: ").strip()
    methods = [m.strip() for m in methods_input.split(",")] if methods_input else ["filesystem","command","desktop"]
    output_type = input("출력 방식 선택 (print/file/all) [기본: all]: ").strip() or "all"
    outputfile_name = input("출력 파일 이름 [기본: output.txt]: ").strip() or "output.txt"
    roots_input = input("탐색할 디렉터리 쉼표 구분 (기본: PATH): ").strip()
    roots = [r.strip() for r in roots_input.split(",")] if roots_input else None
    include_all = input("실행 불가능한 파일 포함? (y/n) [기본: n]: ").strip().lower() == "y"
    include_similar_file = input("정확히 같지 않은 파일도 탐색? (y/n) [기본: n]: ").strip().lower() == "y"

    search_program(name, methods, roots, include_all, include_similar_file, output_type, outputfile_name)
