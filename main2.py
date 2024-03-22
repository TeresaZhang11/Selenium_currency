from collections import deque

#function to check valid parenthesis
def paren_checker(input: str) -> str:
    ans = ""
    stk = deque()
    for c in input:
        #如果是左括号 先加到栈上 输出先加‘x' 后面遇到右括号再进一步处理
        if c == '(':
            ans += 'x'
            stk.append(c)
        #遇到右括号
        elif c == ')':
            #如果空栈 直接加
            if not stk:
                ans += '?'
                stk.append(c)
                continue
            #如果不是空栈 检查左括号是否存在
            top = stk[-1]
            if top == '(':
                stk.pop()
                #找到输出里面最后一个x 用‘  ’代替
                lastx = ans.rfind('x')
                ans = ans[:lastx] + ' ' + ans[lastx+1: ]
            else:
                #前面还是右括号 消不掉
                ans += '?'
                stk.append(c)
                
        #忽视除括号以外的字符       
        else:
            ans += ' '
    ans = input + '\n' + ans
    return ans

def main():
    inputs = ['bge)))))))))', '((IIII))))))', '()()()()(uuu', '))))UUUU((()']
    for input in inputs:
        print(paren_checker(input))
    # ans = paren_checker('bge)))))))))')
    # print(ans)

if __name__ == "__main__":
    main()