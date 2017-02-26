#排除重复的生成器，可针对多种序列,如果元素不可哈希，则传入key函数，一般用匿名函数
def dedupe(items,key=None):
    seen=set()
    for item  in items:
        val=item if key is None else key(item)
        if val not in seen:
            yield item
            seen.add(val)