from multiprocessing import Process , Queue , current_process
import sys
def encoding(text,s):
    abc = "abcdefghijklmnopqrstuvwxyz"
    encodedAbc = (abc[s:len(abc)] + abc[0:s]).upper()
    
    str = ""
    for c in text:
        try:
            x =abc.index(c)
            str += encodedAbc[x]
        except:
            str += c
    return str
        

def worker(queue,processedQueue,s,mainIndex):
#    print(current_process().name + " started :" )
    try:
        print(str(queue.empty()) + " " + current_process().name)
        
        while not queue.empty():
            try:
                data = queue.get()
    #            print(current_process().name + " log ::" + str(mainIndex)+ " "  + str(data))
    #            none
                processedQueue.put({"text":encoding(data["text"],s),"index":data["index"]})
            except Exception as err:
                print(str(err) + " " +current_process().name)
                break
        
        print(str(queue.empty()) + " " + current_process().name)
        print(current_process().name + " ended ")
    except Exception as err:
        print(str(err) + " " +current_process().name)
        
    return True


if __name__ == '__main__':
    if len(sys.argv) != 4:
        print("invalid argument")
        print("script.py <s> <n> <l>")
        exit()
    s = int(sys.argv[1])
    n = int(sys.argv[2])
    l = int(sys.argv[3])
    
    
    f = open("./input.txt","r")
    text = f.read().lower()
    
    queue = Queue()
    processedQueue = Queue()
    
        
    pr = []
    
    tmp = 0
    index = 0
    #queueLock.acquire()
    while True:
        if tmp >= len(text):
            break
#        print(text[tmp:tmp+l])
        queue.put({"text":text[tmp:tmp+l],"index":index})
        tmp = tmp + l
        index += 1
        
    for i in range(0,n):
        p = Process(target=worker, args=(queue,processedQueue,s,i))
        p.start()
        pr.append(p)
#        queue.put("STOP")
    
    
    for p in pr:
        p.join()
    
    
    mergeArray = [None]*index

    while not processedQueue.empty():
        data = processedQueue.get()
        mergeArray[data["index"]] = data["text"]

    encodedText = ""
    for str in mergeArray:
        encodedText += str
    f = open("crypted_fork_11_16_8.txt","w")
    f.write(encodedText)
    print("Exiting main thread")

