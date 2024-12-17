package main

import (
	"fmt"
	"log"
	"os"
	"sort"
	"strconv"
	"strings"
)

func seqOk(seq []string, mustComeAfter map[string][]string, key string) bool {
	mustComeAfterVals, keyExists := mustComeAfter[key]
	if len(seq) == 0 || !keyExists {
		return true
	}
	for _, next := range seq {
		for _, mustComeAfterVal := range mustComeAfterVals {
			if next == mustComeAfterVal {
				return false
			}
		}
	}
	return true
}

func SeqOk(seq []string, mustComeAfter map[string][]string) bool {
	for i, step := range seq {
		if !seqOk(seq[i+1:], mustComeAfter, step) {
			return false
		}
	}
	return true
}

func FixSeq(seq *[]string, mustComeAfter map[string][]string) {
	sort.SliceStable(*seq, func(i, j int) bool {
		a := (*seq)[i]
		b := (*seq)[j]
		if vals, ok := mustComeAfter[a]; ok {
			for _, val := range vals {
				if val == b {
					return false
				}
			}
		}
		return true
	})
}

func main() {
	content, err := os.ReadFile("in2.txt")
	if err != nil {
		log.Fatalf("unable to read file: %v", err)
	}
	lines := strings.Split(string(content), "\n")
	var parseRules bool = true
	var mustComeAfter map[string][]string = make(map[string][]string)
	var seqs [][]string = make([][]string, 0)

	for _, line := range lines {
		if strings.TrimSpace(line) == "" {
			parseRules = false
		} else {
			if parseRules {
				ruleParts := strings.Split(line, "|")
				mustComeAfter[ruleParts[1]] = append(mustComeAfter[ruleParts[1]], ruleParts[0])
			} else {
				seqs = append(seqs, strings.Split(line, ","))
			}
		}
	}

	var okSeqs []bool = make([]bool, 0)
	var correctSeqSum, incorrectSeqSum int = 0, 0
	for _, seq := range seqs {
		okSeqs = append(okSeqs, SeqOk(seq, mustComeAfter))
	}

	// var fixedSeqs [][]string = make([][]string, 0)
	for ndx, ok := range okSeqs {
		if ok {
			seq := seqs[ndx]
			midVal, _ := strconv.Atoi(seq[len(seq)/2])
			correctSeqSum += midVal
		} else {
			seq := seqs[ndx]
			// fmt.Println("bef=", seq)
			FixSeq(&seq, mustComeAfter)
			// fmt.Println("aft=", seq)
			// fixedSeqs = append(fixedSeqs, seqs[ndx])
			midVal, _ := strconv.Atoi(seq[len(seq)/2])
			incorrectSeqSum += midVal
		}
	}

	fmt.Println("Part 1 correctSeqSum =", correctSeqSum)
	fmt.Println("Part 2 incorrectSeqSum =", incorrectSeqSum) //, fixedSeqs)
}
