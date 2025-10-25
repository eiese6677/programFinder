import os
import re

def find_similar_programs(target_name, roots=None, include_all=False):
    """지정된 디렉터리(기본값: '/', '/bin', '/usr') 내에서 target_name을 포함하는 실행 파일 검색"""
    if roots is None:
        roots = os.environ["PATH"].split(":")
    elif isinstance(roots, str):
        roots = [roots]

    matched = []
    pattern = re.compile(f".*{re.escape(target_name)}.*", re.IGNORECASE)

    for directory in roots:
        if not os.path.isdir(directory):
            continue
        for current_root, _, files in os.walk(directory):
            try:
                for file_name in files:
                    if pattern.match(file_name):
                        full_path = os.path.join(current_root, file_name)
                        if not include_all:
                            # 실행 가능한 파일만 출력
                            if os.access(full_path, os.X_OK):
                                matched.append(full_path)
                        else:
                            matched.append(full_path)
            except (PermissionError, OSError):
                # 권한 없거나 파일 접근 불가한 폴더 무시
                continue

    return matched


def search_program(name, roots=None, output_type="all", outputfile_name="output.txt",include_all=False):
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
            print(f"Searching for '{name}' in filesystem (root = {roots}) (this may take a while)...")
    else:
        search_dirs = os.environ["PATH"].split(":")
        if do_print:
            print(f"Searching for '{name}' in PATH directories (this may take a while)...")

    # 검색 실행
    found_paths = find_similar_programs(name, search_dirs, include_all=include_all)
    result.extend(found_paths)

    # 결과 출력
    if do_print:
        print()
        if found_paths:
            print(*found_paths, sep="\n")
        else:
            print("No matching files found.  Try searching in /")

    # 파일 저장
    if do_file:
        with open(outputfile_name, "a", encoding="utf-8") as f:
            f.write("\n".join(result) + "\n")
            if not found_paths:
                f.write("No matching files found. Try searching in /\n")

    return found_paths
