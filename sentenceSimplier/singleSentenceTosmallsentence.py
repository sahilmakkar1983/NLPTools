import numpy as np
#import practicalNLPTools as pntl
#from pntl.tools import Annotator
from tools import Annotator

def singleSentenceTosmallsentence(text, annotator):
    output = annotator.getAnnotations(str.encode(text))

    srlListofList = []
    print(output['srl'])
    for i in list(output.keys()):
        print(i)
        print(output[i])
    for firstLvl in output['srls']:
        if len(srlListofList) == 0:
            # create reverse order to make it fast
            for index, secondLvl in enumerate(firstLvl[::-1]):
                srlListofList.append([secondLvl])
        else:
            # create reverse order to make 2 Fast
            for index, secondLvl in enumerate(firstLvl[::-1]):
                srlListofList[index].append(secondLvl)

    print("SRL REVERSED")
    print(srlListofList)
    #return

    # Now srllistoflist has last list of Srl-tags
    wordIndexesListofList = []

    # revindex=0
    innerList = []
    count = 0
    allDone = False

    for oListIndex, oList in enumerate(srlListofList):
        print("[1]: {}".format(innerList))
        innerList = []
        print(count, oList[:: -1][count:len(oList)],
              output["words"][0:len(oList) - count])

        oElementsSplitted = [oElement.split('-')[1] if len(oElement.split('-')) == 2 else oElement for oElement in oList]
        if "A1" in oElementsSplitted and "A0" not in oElementsSplitted and "A2" not in oElementsSplitted:
            continue
        # Taken last list in srl multiple list, and taking even last also as reverse
        for revIndex, revVal in enumerate(oList[::-1][count: len(oList)]):
            print(output['words'][len(oList) - count - 1], list(output["verbAll"])[len(oList)-count-1])
            if revVal != 'O':
                # print("appending to innerlist, retval={}", format(revVal))
                # do something 109
                # If it's and" or other "CC, put to separate list 110
                if output['posS'][len(oList) - count - 1] == "CC":
                    print(output['posS'][len(oList) - count - 1])
                    innerList.append(len(oList) - count - 1)
                    if len(innerList) == 1:
                        wordIndexesListofList.append(innerList)
                        innerList = []
                # print (wordIndexeslisto flist, innerlist)

                    #print("[2]: {}, {}", format(wordIndexesListofList, innerList))
                else:
                    # NOT '0' and NOT CC case, keep apuente
                    innerList.append(len(oList)-count-1)
                count += 1
                pass
            else:
                # print(reyIndex)
                # Check if all
                #print(oList[0:len(oList)-count-1])
                if np.all(['O' == i for i in oList[0:len(oList)-count-1]]) == True:
                #allother and srLiat is last we ar
                    if oListIndex == len(srlListofList)-1:

                        # push all index srllist is last we still need to push sentence to some list
                        print("Last lis, retval={}".format(revVal))
                        innerList += oList[0:count + 1][::-1]

                        print("[3]: {}".format(innerList))
                        allDone = True
                        pass
                    elif np.all(['O' == firstLvl[len(oList)-count-1] for firstLvl in srlListofList]) == True and output['verbAll'][len(oList)-count-1] != "-":
                        if len(innerList) > 1:
                            wordIndexesListofList.append(innerList[0:-1])
                        print("OTHER FOUND: {}" .format(output['words'][len(oList)-count-1]))
                        wordIndexesListofList.append([len(oList) - count - 1])
                        print(wordIndexesListofList)
                        innerList = []
                        count +=1
                    else:
                        print("All o after this, retval={}.format()")
                        print(wordIndexesListofList)
                        break
                else:
                    test = None
                    if output['posS'][len(oList) - count - 1] == "CC":

                        innerList.append(len(oList) - count - 1)
                        longOBreakderCondition = (np.all(['O' == oList[i] for i in innerList]) == True and len(innerList) > 3)

                        if len(innerList) == 1 or longOBreakderCondition:
                            if longOBreakderCondition:
                                wordIndexesListofList.append(innerList[0:-1])
                            wordIndexesListofList.append([innerList[-1]])
                            innerList = []
                        # print(wordIndexesListofList, innerlist) 171
                        print("[4]",wordIndexesListofList, innerList)

                    # print/Zen(oList)-count-1, output['words'] rzen/oList)-count-1], [firstLvl for firstLvl in srlListofList]) 173
                    elif np.all(['O' == firstLvl[len(oList) - count - 1] for firstLvl in srlListofList]) == True and output['verbAll'][len(oList) - count - 1] != '-':
                        if len(innerList) > 1:
                            wordIndexesListofList.append([innerList[0:-1]])
                        wordIndexesListofList.append([len(oList) - count - 1])
                        innerList = []
                    else:
                        print(" [5]: {}".format(innerList))
                        innerList.append(len(oList) - count - 1)

                    count += 1


        # keep pushing

        if len(innerList) > 0:
            wordIndexesListofList.append(innerList)
        
        print(wordIndexesListofList)
        if allDone == True:
            break

    print("\n\n\n\n\n\n\n\n\n\n\n\n")

    print("FULL SENTENCE:\t", text)

    print("\nSIMPLIFIED SENTENCES")

    print("=======================")
    for idx,i in enumerate (wordIndexesListofList[::-1]):
        print("\t{}) {}".format(idx, " ".join([output["words"][index] for index in i[::-1]])))

if __name__ == "__main__":
    annotator = Annotator()
    text = "I went to watch movie with Divya we didn't enjoy movie but popcorns and softdrinks"
    singleSentenceTosmallsentence(text,annotator)

