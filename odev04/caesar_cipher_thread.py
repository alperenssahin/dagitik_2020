import sys
import queue
import threading

class Worker(threading.Thread):
    def __init__(self,queue):
        threading.Thread.__init__(self)
        self.queue = queue
    def run(self):
        process_queue(self.queue)
            
def encoding(text):
    str = ""
    for c in text:
        try:
            x =abc.index(c)
            str += encodedAbc[x]
        except:
            str += c
        
    return str
        

def process_queue(queue):
    while True:
        queueLock.acquire()
        if not queue.empty():
            data =queue.get()
            queueLock.release()
            processedQueue.put({"text":encoding(data["text"]),"index":data["index"]})
        else:
            queueLock.release()
            break
            
if len(sys.argv) != 4:
    print("invalid argument")
    print("script.py <s> <n> <l>")
    exit()
s = int(sys.argv[1])
n = int(sys.argv[2])
l = int(sys.argv[3])

f = open("./input.txt","r")


text = f.read().lower()

abc = "abcdefghijklmnopqrstuvwxyz"

encodedAbc = (abc[s:len(abc)] + abc[0:s]).upper()

wordQueue = queue.Queue(int(len(text)/l) + 1 )
processedQueue = queue.Queue(int(len(text)/l) + 1 )
queueLock = threading.Lock()


tmp = 0
index = 0
queueLock.acquire()
while True:
    if tmp >= len(text):
        break
    wordQueue.put({"text":text[tmp:tmp+l],"index":index})
    tmp = tmp + l
    index += 1
queueLock.release()


threads = []
ThreadCount = 0

while True:
    thread = Worker(wordQueue)
    thread.start()
    threads.append(thread)
    ThreadCount += 1
    if ThreadCount == n:
        break
    
    
for thread in threads:
    thread.join()
    
mergeArray = [None]*index

while not processedQueue.empty():
    data = processedQueue.get()
    mergeArray[data["index"]] = data["text"]

encodedText = ""
for str in mergeArray:
    encodedText += str
f = open("crypted_thread_15_14_32.txt","w")
f.write(encodedText)
print("Exiting main thread")
