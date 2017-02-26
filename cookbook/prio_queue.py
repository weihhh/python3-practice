import heapq
#第一个 pop() 操作返回优先级最高的元素。另外注意到如果两个有着相同优先级的元素 ( foo 和 grok )， pop 操作按照它们被插入到队列的顺序返回的。
class PriorityQueue:
    def __init__(self):
        self._queue=[]
        self._index=0
        
    def push(self,item,priority):
        heapq.heappush(self._queue,(-priority,self._index,item))#堆数据结构最重要的特征是 heap[0] 永远是最小的元素。heappush方法根据后面元素的大小，总是将最小的元素放置在第一位，然后heappop函数总是将第一位元素弹出
        #上面的元组排序，先利用优先级变量，再用index值
        self._index+=1
    
    def pop(self):
        return heapq.heappop(self._queue)[-1]#上面的优先级priority前面的负号使得优先级高的先弹出，index保证当优先级相同时先压进的先弹出
        
#试验       
q=PriorityQueue()
q.push('foo',5)
print(q._queue)
q.push('oll',4)
print(q._queue)
print(q.pop())
print(q._queue)