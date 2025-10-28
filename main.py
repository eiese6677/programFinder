#!/usr/bin/env python3
import FindPackage as fp
from findInPath import search_program

def main():
    # ---------------- 입력 ----------------
    program_name = input("🔍 패키지/프로그램 이름을 입력하세요: ").strip()
    while not program_name:
        program_name = input("❗ 패키지 이름은 필수입니다.: ").strip()

    # 검색 방식 선택
    methods_input = input("🔧 검색 방식 선택 (package/filesystem/command/desktop, 콤마로 구분, 기본: 모두): ").strip()
    methods = [m.strip() for m in methods_input.split(",")] if methods_input else ["package","filesystem","command","desktop"]

    # 출력 형식 선택
    output_type = input("📤 출력 형식을 선택하세요 (print / file / all) [기본값: all]: ").strip().lower()
    if output_type not in ("print","file","all"):
        output_type = "all"

    # 파일 출력 이름
    output_name = "output.txt"
    if output_type in ("file","all"):
        name_input = input("💾 출력 파일 이름을 입력하세요 [기본값: output.txt]: ").strip()
        if name_input:
            output_name = name_input

    # 탐색 루트 디렉터리 입력
    root_input = input("📂 탐색할 디렉터리를 쉼표로 구분해 입력하세요 [기본값: PATH]: ").strip()
    root = [r.strip() for r in root_input.split(",")] if root_input else None

    # 옵션
    include_all = input("실행 불가능한 파일도 포함? (y/n) [기본값: n]: ").strip().lower() == "y"
    include_similar_file = input("정확히 같지 않은 파일도 탐색? (y/n) [기본값: n]: ").strip().lower() == "y"

    # ---------------- 요약 ----------------
    print("\n⚙️ 설정 요약")
    print(f" - 패키지/프로그램 이름: {program_name}")
    print(f" - 검색 방식: {', '.join(methods)}")
    print(f" - 출력 형식: {output_type}")
    print(f" - 출력 파일: {output_name}")
    print(f" - 탐색 경로: {root if root else 'PATH 환경변수 사용'}")
    print(f" - 실행 불가능한 파일 {'포함' if include_all else '제외'}")
    print(f" - 정확히 같지 않은 파일 {'포함' if include_similar_file else '제외'}\n")

    # ---------------- 검색 실행 ----------------
    if "package" in methods:
        fp.findPackage(
            program_name,
            output_type=output_type,
            outputfile_name=output_name
        )

    # 나머지 검색
    other_methods = [m for m in methods if m != "package"]
    if other_methods:
        search_program(
            program_name,
            methods=other_methods,
            roots=root,
            include_all=include_all,
            include_similar_file=include_similar_file,
            output_type=output_type,
            outputfile_name=output_name
        )

if __name__ == "__main__":
    main()
