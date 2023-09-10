import hashlib

#-------------Merkle Tree including hashing values------------#
#encodes strings in utf-8 format so it can be properly hashed
def compute_hash(data):
    if isinstance(data, str):
        data = data.encode('utf-8')
    sha256 = hashlib.sha256()
    sha256.update(data)
    return sha256.digest()

#creates a merkle tree by first converting all items to an encrypted hash and then
#passing that into build_merkle_tree which recursively builds the tree upward
#each level is stored in results so we can visualize the tree
def merkle_tree(item_list):
    def build_merkle_tree(node_list,results):
        #error condition, if no items are passed in print error and return
        if len(node_list) == 0:
            print('Error: 0 items passed in')
            return None

        #exit condition, if there's only 1 item left it will be the merkle root
        if len(node_list) == 1:
            return (node_list[0].hex(),results)
        
        #first pass through append the initial node_list, which is our bottom-most layer
        if len(results) == 0:
            results.append(node_list)

        next_level = []

        #for every 2 nodes combine their hashes and then encrypt and add it onto the next level
        for i in range(0, len(node_list), 2):
            left = node_list[i]

            #handle odd amounts of nodes
            if i + 1 < len(node_list):
                right = node_list[i + 1]
            else:
                right = compute_hash('') 

            combined_hash = compute_hash(left + right)
            next_level.append(combined_hash)

        #add the next level to the results and do a recursive call to build the next level
        results.append(next_level)
        return build_merkle_tree(next_level,results)
    
    #converts all items into a hash before building
    hashes = []
    for item in item_list:
        hashes.append(compute_hash(item))

    #initial call to build the merkle tree with our hash-list and an empty result array
    tree = build_merkle_tree(hashes,[])
    return tree
    
#-------------Merkle Tree NOT hashing values------------#
def merkle_tree_no_hash(item_list):
    def build_merkle_tree(node_list,results):
        if len(node_list) == 0:
            return None

        if len(node_list) == 1:
            return (node_list[0],results)
        
        if len(results) == 0:
            results.append(node_list)

        next_level = []

        for i in range(0, len(node_list), 2):
            left = node_list[i]

            if i + 1 < len(node_list):
                right = node_list[i + 1]
            else:
                right = ''

            combined_hash = left + right
            next_level.append(combined_hash)

        results.append(next_level)
        return build_merkle_tree(next_level,results)
    
    tree = build_merkle_tree(item_list,[])
    return tree

#----------Prints a rough visualization of the tree-------#
#only for use with merkle_tree_no_hash
def printTree(tree_list):
    def reverseList(arr):
        out_list = []
        for i in reversed(arr):
            out_list.append(i)
        return out_list
    
    tree_list = reverseList(tree_list)
    level_str = '\t'
    for level in tree_list:
        for node in level:
            level_str = level_str + '-' + node
        print(level_str)
        level_str = '\t'
    print('')

#--------------------------------------------------------#     
#   I've included two functions merkle_tree(item_list) and merkle_tree_no_hash(item_list).
# Both return a tuple where the first element is the merkle-root and the second is the result list.
# The result list is a list of lists, where the first item in the list is the bottom-most layer of items, and the
# second item is the layer above the bottom-most and so forth. This way we are able to visualize the structure of the tree.
#
# merkle_tree_no_hash(item_list) builds the merkle tree, but without encrypting the values so we can see it working more clearly

#26 element tree alphabet test no hash
def main():
    print('26 element tree alphabet test no hash')
    alphabet = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
    merkle = merkle_tree_no_hash(alphabet)
    root = merkle[0]
    results = merkle[1]
    print('The merkle root is: ' + root)
    printTree(results)

    #8 element tree test no hash
    print('8 element tree - no hash')
    test = ['a','b','c','d','e','f','g','h']
    merkle = merkle_tree_no_hash(test)
    root = merkle[0]
    results = merkle[1]
    print('The merkle root is: ' + root)
    printTree(results)

    #11 element tree test no hash
    print('11 element tree - no hash')
    test = ['p','q','r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
    merkle = merkle_tree_no_hash(test)
    root = merkle[0]
    results = merkle[1]
    print('The merkle root is: ' + root)
    printTree(results)

    #create two identical 4 item merkle tree and confirm merkle roots are equal
    transaction_ids1 = ['a','b','c','d']
    transaction_ids2 = ['a','b','c','d']
    merkle1 = merkle_tree(transaction_ids1)
    merkle2 = merkle_tree(transaction_ids2)
    root1 = merkle1[0]
    root2 = merkle2[0]
    print(root1 + ' does equal ' + root2)

    #create a 4 and 5 item merkle tree and confirm the merkle roots differ
    transaction_ids1 = ['a','b','c','d']
    transaction_ids2 = ['a','b','c','d','e']
    merkle1 = merkle_tree(transaction_ids1)
    merkle2 = merkle_tree(transaction_ids2)
    root1 = merkle1[0]
    root2 = merkle2[0]
    print(root1 + ' does not equal ' + root2)


    #create two 4 item merkle trees, but with one element differing, and confirm merkle roots differ
    transaction_ids1 = ['a','b','c','d']
    transaction_ids2 = ['a','b','c','f']
    merkle1 = merkle_tree(transaction_ids1)
    merkle2 = merkle_tree(transaction_ids2)
    root1 = merkle1[0]
    root2 = merkle2[0]
    print(root1 + ' does not equal ' + root2)

main()
