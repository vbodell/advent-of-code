class MapHandler
  DIRS = [[0,1], [1,1], [1,0], [1,-1], [0,-1], [-1,-1], [-1,0], [-1,1]]
  XDIRS = [[-1, -1], [1,1], [1,-1], [-1, 1]]
  
  def parse(fname)
    if fname == nil
      puts "No filename specified.\nUsage: ruby #{$0} <filename>"
      return
    end
    lines = File.read(fname).split
    @data = lines.each do |line|
      line.chars.each do |char| char
      end
    end
  end

  def inBounds(i,j)
    return i >= 0 && j >= 0 && i < @data.size && j < @data[i].size
  end
  
  def findWithDir(i,j,val,dir)
    # print i,j,val,dir
    # puts
    nexti = i+dir[0]
    nextj = j+dir[1]
    if inBounds(nexti,nextj) && @data[nexti][nextj] == val
      case val
      when "M"
        return findWithDir(nexti, nextj, "A", dir)
      when "A"
        return findWithDir(nexti, nextj, "S", dir)
      when "S"
        return true
      end
    end
    return false
  end

  def findFrom(i,j,val)
    found = 0
    DIRS.each do |dir|
      if findWithDir(i,j,val,dir)
        found += 1
      end
    end
    return found
  end

  def findxmas()
    found = 0
    @data.each_with_index do |row,i|
      row.chars.each_with_index do |col,j|
        if col == "X"
          newfound = findFrom(i,j,"M")
          # print i,j,newfound
          # puts
          found += newfound
        end
      end
    end
    return found
  end

  def findCrossFrom(i,j)
    if !(inBounds(i-1, j-1) && inBounds(i+1, j+1))
      return false
    end
    checks = XDIRS.map { |dir| @data[i+dir[0]][j+dir[1]] }
    if (checks[0] == "M" && checks[1] == "S" 
        || checks[0] == "S" && checks[1] == "M") 
      && (checks[2] == "M" && checks[3] == "S" 
          || checks[2] == "S" && checks[3] == "M")
      return true
    end
    return false
  end

  def findcrossmas()
    found = 0
    @data.each_with_index do |row,i|
      row.chars.each_with_index do |col,j|
        if col == "A" && findCrossFrom(i,j)
          found += 1
        end
      end
    end
    return found
  end
end


if __FILE__ == $0
  handler = MapHandler.new
  handler.parse ARGV[0]
  puts "xmas-found=#{handler.findxmas}"
  puts "cross-mas-found=#{handler.findcrossmas}"
end
