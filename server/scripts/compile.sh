code_path="$1"
language_name="$2"
before_compile_file_name="$3"
after_compile_file_name="$4"
sandbox build --language "$language_name" --input "$code_path/$before_compile_file_name" --output "$code_path/$after_compile_file_name"