use std::fs::File;
use std::io::{self, BufRead};

fn next_dir(dir: (i32, i32)) -> (i32, i32) {
    if dir == (-1, 0) {
        return (0, 1);
    } else if dir == (0, 1) {
        return (1, 0);
    } else if dir == (1, 0) {
        return (0, -1)
    } else {
        return (-1, 0)
    }
}

fn next_dir_indexed(dir: (i32, i32, usize)) -> (i32, i32, usize) {
    if dir == (-1, 0, 0) {
        return (0, 1, 1);
    } else if dir == (0, 1, 1) {
        return (1, 0, 2);
    } else if dir == (1, 0, 2) {
        return (0, -1, 3)
    } else {
        return (-1, 0, 0)
    }
}


fn simulate_obstacle(map: &Vec<Vec<char>>) -> bool {
    let mut pos: (usize, usize) = (0,0);
    let mut dir: (i32, i32, usize) = (0,0,0);
    let mut guardleft = false;
    let mut guardloops = false;
    let mut t = 0;
    let rows = map.len();
    let cols = map[0].len();

    let mut dirs_visited = vec![vec![vec![false; 4]; cols]; rows];
    for (i, row) in map.iter().enumerate() {
        for (j, ch) in row.iter().enumerate() {
            if *ch == '^' {
                pos = (i,j);
                dir = (-1, 0, 0);
            }
        }
    }

    let inbounds = |pos: (i32, i32)| -> bool {
        return pos.0 >= 0 && (pos.0 as usize) < rows && pos.1 >= 0 && (pos.1 as usize) < cols
    };

    let collides = |point: char| -> bool {
        return point == '#'
    };

    while !guardleft && !guardloops {
        // map[pos.0][pos.1] = 'X';
        dirs_visited[pos.0][pos.1][dir.2] = true;
        loop {
            let trynextpos = (pos.0 as i32 + dir.0, pos.1 as i32 + dir.1);
            let nextpos: (usize, usize);

            if inbounds(trynextpos) {
                nextpos = (trynextpos.0 as usize, trynextpos.1 as usize);
            } else {
                guardleft = true;
                break;
            }

            if !collides(map[nextpos.0][nextpos.1]) {
                pos = nextpos;
                break;
            }
            dir = next_dir_indexed(dir);
        }

        if !guardleft && dirs_visited[pos.0][pos.1][dir.2] {
            guardloops = true
        }
        t += 1;

        // println!("t={}", t);
        // for row in &map {
        //     println!("{:?}", row)
        // }
    }
    return guardloops
}

fn simulate(map: &mut Vec<Vec<char>>) {
    let mut pos: (usize, usize) = (0,0);
    let mut dir: (i32, i32) = (0,0);
    let mut guardleft = false;
    let rows = map.len();
    let cols = map[0].len();
    for (i, row) in map.iter().enumerate() {
        for (j, ch) in row.iter().enumerate() {
            if *ch == '^' {
                pos = (i,j);
                dir = (-1, 0);
            }
        }
    }

    let inbounds = |pos: (i32, i32)| -> bool {
        return pos.0 >= 0 && (pos.0 as usize) < rows && pos.1 >= 0 && (pos.1 as usize) < cols
    };

    let collides = |point: char| -> bool {
        return point == '#'
    };

    while !guardleft {
        map[pos.0][pos.1] = 'X';
        loop {
            let trynextpos = (pos.0 as i32 + dir.0, pos.1 as i32 + dir.1);
            let nextpos: (usize, usize);
            if inbounds(trynextpos) {
                nextpos = (trynextpos.0 as usize, trynextpos.1 as usize);
            } else {
                guardleft = true;
                break;
            }

            if !collides(map[nextpos.0][nextpos.1]) {
                pos = nextpos;
                map[nextpos.0][nextpos.1] = '&';
                break;
            }
            dir = next_dir(dir);
        }

        // println!("t={}", t);
        // for row in &mut *map {
        //     println!("{:?}", row)
        // }
    }
}

fn count(map: &Vec<Vec<char>>, target: char) -> usize {
    map.iter().flat_map(|row| row.iter()).filter(|&&c| c == target).count()
}

fn main() -> std::io::Result<()> {
    let file = File::open("in.txt")?;
    let reader = io::BufReader::new(file);
    let mut prev = (0,0);
    let mut loops = 0;
    let mut previnit = false;

    let mut map: Vec<Vec<char>> = Vec::new();
    for line in reader.lines() {
        let line = line?;
        let row: Vec<char> = line.chars().collect();
        map.push(row);
    }

    // simulate(&mut map);

    // println!("sum={}", count(&map, 'X'));

    for i in 0..map.len() {
        for j in 0..map[i].len() {
            if map[i][j] != '#' && map[i][j] != '^' {
                map[i][j] = '#';
                if !previnit {
                    previnit = true;
                } else {
                    map[prev.0][prev.1] = '.';
                }
                prev = (i, j);
                if simulate_obstacle(&map) {
                    loops += 1;
                }
            }
        }
    }

    println!("count={}", loops);

    Ok(())
}
