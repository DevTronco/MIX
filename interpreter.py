def run_file(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        code = f.read()
    print(f" File content: '{code}'")
    run_code(code)

def run_code(code):
    lines = [l.strip() for l in code.strip().split("\n") if l.strip()]
    print(f" Parsed lines: {lines}")
    env = {}
    i = 0

    def eval_expr(expr):
        print(f" Evaluating expression: '{expr}'")
        try:
            # number
            if expr.isdigit():
                result = int(expr)
                print(f" Number result: {result}")
                return result
            
            # string
            if expr.startswith('"') and expr.endswith('"'):
                result = expr[1:-1]  # removes ""
                print(f" String result: '{result}'")
                return result
            
            # variable
            if expr in env:
                result = env[expr]
                print(f" Variable result: {result}")
                return result
            
            # concatenation
            if "+" in expr:
                parts = expr.split("+")
                result = ""
                for part in parts:
                    part = part.strip()
                    if part.startswith('"') and part.endswith('"'):
                        result += part[1:-1]
                    elif part in env:
                        result += str(env[part])
                    else:
                        result += str(part)
                print(f"Concatenation result: '{result}'")
                return result
            
            # fallback
            result = eval(expr, {}, env)
            print(f"Eval result: {result}")
            return result
            
        except Exception as e:
            print(f"Error in eval_expr: {e}")
            return expr

    while i < len(lines):
        line = lines[i]
        print(f"Processing line {i}: '{line}'")

        if line.startswith("var"):
            print("Found variable declaration")
            var_line = line[4:].rstrip(";")
            print(f"After removing 'var' and ';': '{var_line}'")
            
            if "=" in var_line:
                var, value = var_line.split("=", 1) 
                var_name = var.strip()
                var_value = value.strip()
                print(f"Variable name: '{var_name}', value: '{var_value}'")
                
                env[var_name] = eval_expr(var_value)
                print(f"Environment updated: {env}")
            else:
                print("No '=' found in variable declaration")
        
        #comment
        elif line.startswith("::"):
            print("Comment identified!")
        
        #print
        elif line.startswith("print"):
            print("Found print statement")
            expr = line[5:].strip()  
            if expr.endswith(";"):
                expr = expr[:-1]  
            print(f"Expression to print: '{expr}'")
            
            result = eval_expr(expr)
            print(f"FINAL OUTPUT: {result}")

        #if
        elif line.startswith("if"):
            print("Found if statement")
            start = line.find("(")
            end = line.find(")")
            if start != -1 and end != -1:
                condition = line[start+1:end]
                print(f"🔍 Condition: '{condition}'")
                block = []
                i += 1
                brace_count = 0
                while i < len(lines):
                    current_line = lines[i]
                    if current_line == "{":
                        brace_count += 1
                    elif current_line == "}":
                        if brace_count == 0:
                            break
                        brace_count -= 1
                    elif brace_count > 0:
                            block.append(current_line)
                    i += 1
                
                print(f"🔍 If block: {block}")
                
                try:
                    if "==" in condition:
                        left, right = condition.split("==")
                        left = left.strip()
                        right = right.strip()
                        left_val = eval_expr(left)
                        right_val = eval_expr(right)
                        
                        condition_result = left_val == right_val
                        print(f"Condition '{left_val} == {right_val}' = {condition_result}")
                        
                        if condition_result:
                            print("Condition is TRUE, executing if block")
                            run_code("\n".join(block))
                        else:
                            print("Condition is FALSE, skipping if block")
                    
                except Exception as e:
                    print(f"Error evaluating condition: {e}")
            else:
                print("Could not find condition in parentheses")
        
        #else (needs to be finished)
        elif line.startswith("else"):
            else_block = []
            print("Found 'else' statement!")
            while i < len(lines):
                current_line = lines[i]
                if current_line == "{":
                    brace_count += 1
                elif current_line == "}":
                    brace_count -= 1
                if brace_count == 0:
                    print("Else statement can work!")
                if brace_count > 0:
                    else_block.append(current_line)
                
        i += 1

#test
if __name__ == "__main__":
    test_code = '''var x = 15;
if (x == 15) {
    print x;
} else {
    print "x non é 15 ma " + x;
}'''
    
    print("Starting MIX interpreter...")
    run_code(test_code)