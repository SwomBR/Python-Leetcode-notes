#PYTHON NOTES- https://github.com/WeCode-Community-Dev/FAANG-Coding-Interview-Questions/blob/main/TopLeetCodeProblems.md


##Problem waise (Array)
*problem 1* (Two Sum)
https://leetcode.com/problems/two-sum/description/
You are given an array of integers nums and an integer target, return indices of the two numbers such that they add up to target.

You may assume that each input would have exactly one solution, and you may not use the same element twice.

You can return the answer in any order.

 

Example 1:

Input: nums = [2,7,11,15], target = 9
Output: [0,1]
Explanation: Because nums[0] + nums[1] == 9, we return [0, 1].
Example 2:

Input: nums = [3,2,4], target = 6
Output: [1,2]
Example 3:

Input: nums = [3,3], target = 6
Output: [0,1]
 

Constraints:

2 <= nums.length <= 104
-109 <= nums[i] <= 109
-109 <= target <= 109
Only one valid answer exists.
 

Follow-up: Can you come up with an algorithm that is less than O(n2) time complexity?
logic-

LOGIC_How We Solve It
Instead of guessing blindly and trying every single combination (which would take forever if you have a hundred boxes), we can use a smart trick using our memory.

Look at a box: You open the first box and see the number 2.

Find the partner: You ask yourself, "What number do I need to reach our magic target of 9?" You do the math: 9 minus 2 equals 7. You need a box with 7.

Check your memory: Have you seen a box with 7 yet? Nope, this is your first box!

Remember this box: So, you put 2 in your mental backpack and move to the next box.


SOL-
class Solution {
public:
    vector<int> twoSum(vector<int>& nums, int target) {
        unordered_map<int, int> seen; // Memory map to store numbers and their indices
        
        for (int i = 0; i < nums.size(); i++) { // Loop through each element in the array one by one
            int complement = target - nums[i]; // Calculate the missing number needed to reach the target
            
            if (seen.find(complement) != seen.end()) { // Check if the complement already exists in our map
                return {seen[complement], i}; // If found, return the index of the complement and the current index
            }
            
            seen[nums[i]] = i; // If not found, save the current number and its index into the map for future checks
        }
        
        return {}; // Fallback return statement (required by C++, though the problem guarantees a solution)
    }
};

##CONCEPT
**The Two Sum Concept**
The Two Sum problem requires finding the indices of two distinct numbers in an array that add up to a specific target value.

**The Brute Force Approach ($O(n^2)$)**

* **Check every pair:** Use nested loops to test every possible combination of two numbers until you find the pair that equals the target.
* **Drawback:** This scales poorly. For an array with 10,000 elements, it requires roughly 50 million checks, making it inefficient for large datasets.

**The Optimized Hash Map Approach ($O(n)$)**

* **Single Pass:** Iterate through the array exactly once from left to right.
* **Calculate Complement:** For each number you visit, determine its missing partner by subtracting it from the target (`target - current_number`).
* **Check Memory:** Look inside a hash map (or dictionary) to see if you have already seen that complement earlier.
* **Match Found:** If the complement exists in the hash map, return its stored index alongside your current index.
* **Store for Later:** If the complement is not in the hash map, save the current number and its index into the map, then move to the next element.

**Complexity Breakdown**

* **Time Complexity:** $O(n)$ because hash map lookups and insertions take $O(1)$ average time, and the array is traversed only once.
* **Space Complexity:** $O(n)$ because the hash map stores up to $n$ elements in the worst-case scenario.