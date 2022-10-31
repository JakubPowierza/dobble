from time import time
import sys

def statistics(func):
    def wrapper(*args, **kwargs):
        wrapper.count += 1
        t1 = time()
        result = func(*args, **kwargs)
        t2 = time()
        wrapper.time += t2-t1
        return result
    wrapper.count = 0
    wrapper.time = 0
    return wrapper

def split_chains(chains, n):
    
    num_chains = pow(n, 2)
    deconstructed_chains = [[] for i in range(num_chains)]
    
    for i, chain in enumerate(chains):
        deconstructed_chains[i % num_chains].append(chain)
        
    return deconstructed_chains

@statistics
def new_chain_valid(chain_index, chains, num_chains, step):
    for i in range(0, chain_index):
        element_index = step * num_chains
        
        if chains[element_index + i] != chains[element_index + chain_index]:
            continue
        
        for j in range(step):
            element_index = j * num_chains
            if chains[element_index + i] == chains[element_index + chain_index]:
                return False
    return True

def print_chains(chains, n):
    for chain in split_chains(chains, n):
        print(chain)
        
def print_statistics(func):
    if hasattr(func, "count") and hasattr(func, "time"):
        if func.count:
            print(str(func.__name__) + ": " + str(func.count) + " - " + str(func.time) + " - " + str(func.time / func.count))
        else:
            print(str(func.__name__) + ": " + str(func.count) + " - " + str(func.time) + " - null")
    else:
        print(str(func.__name__) + ": NO STATISTICS")

if __name__ == "__main__":

    k = int(sys.argv[1])
    print("K: " + str(k))
    
    n = k - 1
    chains = [i % n for i in range(pow(n, 2))]

    stack = [ 0 ]
    cache = [ [] ]
    i = 0
    previous_i = -1

    time_1 = time()

    while i < pow(n, 3):
        num_chains = pow(n, 2)
        step = (i // num_chains) + 1
        chain_index = i % num_chains
        
        if i > previous_i:
            for trial_value in range(n):
                if new_chain_valid(chain_index, chains + [trial_value], num_chains, step):
                    cache[-1].append(trial_value)
        
        # print(str(stack))
        
        previous_i = i
        
        if len(cache[-1]) < stack[-1] + 1:
            chains.pop()
            stack.pop()
            cache.pop()
            stack[-1] += 1
            i -= 1
            continue
        
        chains.append(cache[-1][stack[-1]])
        stack.append(0)
        cache.append([])
        i += 1

    time_2 = time()

    print("TOTAL_TIME: " + str(time_2 - time_1))
    print_chains(chains, n)
    print_statistics(new_chain_valid)
    