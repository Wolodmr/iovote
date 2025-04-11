import re

def format_requirements(input_file, output_file):
    """
    Reads an input file containing package paths and their hashes,
    formats the information into a requirements.txt-style output.
    """
    package_hashes = {}
    current_package = None
    line_count = 0

    with open(input_file, 'r') as f:
        for line in f:
            line_count += 1
            line = line.strip()
            
            # Debug: Line content
            print(f"DEBUG: Line Content: {line}")

            if not line:
                continue

            # Match package path
            package_match = re.match(r'.*[/\\]([^/\\]+)-[\d\.]+.*\.whl:', line)
            # Debug: Package match
            print(f"DEBUG: Package Match: {package_match.group(1) if package_match else 'No Match'}")
            
            if package_match:
                current_package = package_match.group(1).replace("_", "-")
                package_hashes.setdefault(current_package, set())
                continue

            # Match hash
            hash_match = re.search(r'--hash=sha256:(.+)', line)
            # Debug: Hash match
            print(f"DEBUG: Hash Match: {hash_match.group(1) if hash_match else 'No Match'}")
            
            if hash_match and current_package:
                hash_value = hash_match.group(1)
                package_hashes[current_package].add(hash_value)

    # Debug output before writing
    print(f"DEBUG: Final Package Hashes: {package_hashes}")

    # Write to output file
    with open('requirements.txt', 'w') as f:
        for package, hashes in package_hashes.items():
            for hash_value in hashes:
                f.write(f"{package} --hash={hash_value}\n")


    print(f"Processed {line_count} lines from {input_file}.")
    print(f"Requirements formatted and saved to {output_file}")

if __name__ == "__main__":
    format_requirements('updated-hashes.txt', r'C:\VS_Code\Camp_programs\Projects\vote_cast\requirements.txt')

