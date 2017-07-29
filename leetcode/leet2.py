class Solution(object):
    def fourSum(self, nums, target):
        """
        :type nums: List[int]
        :type target: int
        :rtype: List[List[int]]
        """
        results=[]
        def findnext(nums,target,pre,i,x,result,results):
        	remaining=target-pre
        	for a,j in enumerate(nums[i+1:]):
        		 
        		if x==3:
        			if a==remaining:
        				results.append(result+[a])
        				break
        			else:
        				continue
        		else:
        			if a<remaining:
        				result.append(a)
        				findnext(nums,target,pre+a,j,x+1,result+[a],results)
        	

        findnext(nums,target,0,-1,0,[],results)
        return results
