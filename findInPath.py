import os, re

def find_similar_programs(target_name, root=["/","/bin","/usr"]):
    matched = []
    pattern = re.compile(f".*{re.escape(target_name)}.*", re.IGNORECASE)

    for directory in root:
        if not os.path.isdir(directory):
            continue
        for current_root, dirs, files in os.walk(directory):
            try:
                for file_name in files:
                    if pattern.match(file_name):
                        full_path = os.path.join(current_root, file_name)
                        if os.access(full_path, os.X_OK):  # 실행 가능 여부 체크
                            matched.append(full_path)
            except PermissionError:
                continue  # 권한 없는 폴더는 무시

    return matched

def search_program(name,roots=[],output_type="all",outputfile_name="output.txt"):
    result = ["\n============= 경로로 찾음 ============="]
    if output_type == "print" or output_type == "all":
            print("\n============= 경로로 찾음 =============")
    if roots and roots[0]:
        if output_type == "print" or output_type == "all":
            print(f"Searching for '{name}' in filesystem (root is {roots}) (this may take a while)...")
        result += find_similar_programs(name,roots)
    else:
        result_paths = os.environ["PATH"].split(":")
        if output_type == "print" or output_type == "all":
            print(f"Searching for '{name}' in filesystem (root is {result_paths}) (this may take a while)...")
        result += find_similar_programs(name,result_paths)
    if output_type == "print" or output_type == "all":
        print("\n")
        if len(result) >= 2:
            print(*result[1:],sep="\n")
        else:
            print("No matching files found.")
    if output_type == "file" or output_type == "all":
        with open(outputfile_name, "a", encoding="utf-8") as f:
            st = ""
            for r in result:
                st += "\n" + r
            f.write(st)
            if len(result) == 1:
                f.write("No matching files found.")
    return result[1:]
