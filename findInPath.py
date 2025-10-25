import os,re

def find_similar_programs(target_name,root=["/","/bin","/usr"]):
    path_dirs = root
    matched = []
    pattern = re.compile(f".*{re.escape(target_name)}.*", re.IGNORECASE)

    for directory in path_dirs:
        if not os.path.isdir(directory):
            continue
        try:
            for file_name in os.listdir(directory):
                if pattern.match(file_name):
                    full_path = os.path.join(directory, file_name)
                    if os.access(full_path, os.X_OK):  # 실행 가능 여부 체크
                        matched.append(full_path)
        except PermissionError:
            # 접근 불가
            continue

    return matched

def search_program(name,roots=[],output_type="all",outputfile_name="output.txt"):
    result = ["\n============= 경로로 찾음 ============="]
    if roots and roots[0]:
        result += find_similar_programs(name,roots)
        if output_type == "print" or output_type == "all":
            print(f"Searching for '{name}' in filesystem (root is {roots}) (this may take a while)...")
    else:
        result_paths = os.environ["PATH"].split(":")
        if output_type == "print" or output_type == "all":
            print(f"Searching for '{name}' in filesystem (root is {result_paths}) (this may take a while)...")
        result += find_similar_programs(name,result_paths)
    if output_type == "print" or output_type == "all":
        if result and result[1]:
            print(*result,sep="\n")
        else:
            print("No matching files found.")
    if output_type == "file" or output_type == "all":
        with open(outputfile_name, "a", encoding="utf-8") as f:
            st = ""
            for r in result:
                st += "\n" + r
            f.write(st)
    return result[1:]
