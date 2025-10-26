
import os, re, sys
import subprocess

def is_executable(full_path):
    """Wine, Flatpak wrapper, 심볼릭 링크 포함 실행 가능 판별"""
    try:
        if not os.path.exists(full_path):
            return False

        # 일반 실행 가능 파일
        if os.path.isfile(full_path) and os.access(full_path, os.X_OK):
            return True

        # 심볼릭 링크인데 대상이 실행 가능하면 포함
        if os.path.islink(full_path):
            target = os.path.realpath(full_path)
            if os.access(target, os.X_OK):
                return True

        # Flatpak 시스템 경로
        if full_path.startswith("/var/lib/flatpak/exports/bin/"):
            return True

        # Flatpak 사용자 설치 경로
        if full_path.startswith(os.path.expanduser("~/.local/share/flatpak/exports/bin/")):
            return True

        # Wine .exe 파일
        if full_path.endswith(".exe") and "/.wine/" in full_path:
            return True

    except OSError:
        return False

    return False

def find_similar_programs(target_name, roots=None, include_all=False, include_similar_file=True):
    """지정된 디렉터리(기본값: PATH) 내에서 target_name을 포함하는 실행 파일 또는 관련 파일 검색"""
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
                    if include_similar_file:
                        pattern = re.compile(f"{re.escape(target_name)}", re.IGNORECASE)
                    else:
                        pattern = re.compile(f"^{re.escape(target_name)}$", re.IGNORECASE)
                    if pattern.match(file_name):
                        full_path = os.path.join(current_root, file_name)
                        if include_all or is_executable(full_path):
                            matched.append(full_path)
            except (PermissionError, OSError):
                continue
    return matched

def fine_with_which(target_name, use_find=False, root='/'):
    if use_find:
        found_programs = subprocess.run(
            ['find', '/', '-name', target_name],
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,  # 에러 숨김
            text=True
            )

    else:
        found_programs = subprocess.run(['which', target_name], capture_output=True, text=True)
    return found_programs.stdout.strip().split('\n')

def search_program(name, roots=None, output_type="all", outputfile_name="output.txt",include_all=False,include_similar_file=True):
    """PATH 또는 지정된 루트에서 실행 파일 검색 후 결과 출력/저장"""
    header = "\n============= 경로로 찾음 ============="
    result = [header]

    # 출력 타입 플래그
    do_print = output_type in ("print", "all")
    do_file = output_type in ("file", "all")

    if do_print:
        print(header)

    # 루트 디렉터리 결정
    if roots and isinstance(roots, list) and roots[0]:
        search_dirs = roots
        if do_print:
            print(f"Searching for '{name}' in filesystem (root = {roots}) (this may take a while)...",end='')
    else:
        search_dirs = os.environ["PATH"].split(":")
        if do_print:
            print(f"Searching for '{name}' in PATH directories (this may take a while)...",end='')
    sys.stdout.flush()

    # 검색 실행
    found_paths = find_similar_programs(name, search_dirs, include_all=include_all, include_similar_file=include_similar_file)
    result.extend(found_paths)

    # 결과 출력
    if do_print:
        # 한 줄 지우기
        sys.stdout.write('\r' + ' ' * 100 + '\r')  # 현재 줄 덮어쓰기
        sys.stdout.flush()
        if found_paths:
            print(*found_paths, sep="\n")
        else:
            print("No matching files found.  Try searching in /\n")

    # 파일 저장
    if do_file:
        with open(outputfile_name, "a", encoding="utf-8") as f:
            f.write("\n".join(result) + "\n")
            if not found_paths:
                f.write("No matching files found. Try searching in /\n")

    # which, find
    header = "\n============= 명령어 검색 ============="
    result = [header]
    found_paths = fine_with_which(name,use_find=include_all,root=search_dirs)
    result.extend(found_paths)

    # 결과 출력
    if do_print:
        print(header)
        if found_paths:
            print(*found_paths, sep="\n")
        else:
            print("No matching files found.\n")
        sys.stdout.flush()

    # 파일 저장
    if do_file:
        with open(outputfile_name, "a", encoding="utf-8") as f:
            f.write("\n".join(result) + "\n")
            if not found_paths:
                f.write("No matching files found.\n")

    return found_paths
