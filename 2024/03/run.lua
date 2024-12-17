local function readfile(fname)
    local file = io.open(fname, "r")
    if not file then
        print("Error: Could not open file!")
        os.exit(1)
    end

    local lines = {}
    for line in file:lines() do
        table.insert(lines, line)
    end
    file:close()
    return lines
end

local function calc(lines, respectFlag)
    local sum = 0
    local doit = true
    for _, line in ipairs(lines) do
        local product = 0
        for i = 1, #line do
            if line:sub(i,i+3) == "do()" then
                doit = true
            elseif line:sub(i,i+6) == "don't()" then
                doit = false
            elseif line:sub(i,i+3) == "mul(" then
                local num1, num2 = string.match(line:sub(i), "^mul%((%d+),(%d+)%)")
                if (doit or not respectFlag) and num1 and num2 then
                    product = tonumber(num1) * tonumber(num2)
                    -- print("product="..product)
                    sum = sum + product
                    -- print("sum="..sum)
                end
            end
        end
    end
    return sum
end

local filename = arg[1]
local lines = readfile(filename)
print(calc(lines, false))
print(calc(lines, true))

