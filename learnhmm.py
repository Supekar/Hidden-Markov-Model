import numpy as np
import sys
import copy
import math


def compute_para(input1, word,tag):
	#read words, tags and input from the files
	with open(input1) as infile:
		input2=[]
		for i in infile:
			input2.append(i)
	with open(word) as wordfile:
		word2=[]
		for i in wordfile:
			

			
			word2.append(i)
			

			
	with open(tag) as tagfile:
		tag2=[]
		for i in tagfile:
			
			tag2.append(i)

	#remove #n from the end of the line
	input3=[]
	for i in input2:
		input3.append(i.strip())

	#print(input3)

	word3=[]
	for i in word2:
		word3.append(i.strip())
	tag3=[]
	for i in tag2:
		tag3.append(i.strip())
	#print(tag3)
	#print(word3)

	
	
	tag_len=len(tag3)
	word_len=len(word3)
	print(len(input3))
	print(word_len)
	print(tag_len)

	#get indices and tags index in matrix

	match_final=[]
	for i in input3:
		match=[]
		current=i
		current1=current.split(' ')
		#print(len(current1))

		for x in current1:
		
			word,tag=x.split('_')
			tag_index=tag3.index(tag)
			word_index=word3.index(word)
			match.append([word_index,tag_index])
		match_final.append(match)
	#print(tag2)
	#print(word2)
	#print(match_final[0])

	p_mat=np.zeros((tag_len))
	trans_mat=np.zeros((tag_len, tag_len))
	emiss_mat=np.zeros((tag_len,word_len))


	print(match_final[0])
	#print(match_final[0][0])


	for ind in match_final:
		p_mat[ind[0][1]]+=1
	#add 1 to each element of 
	p_mat+=1


	p_mat=p_mat/np.sum(p_mat)
	#print(p_mat)
	#calculate transmission matrix
	for ind in match_final:
		temp=[]
		for i in ind:
			temp.append(i[1])
		for i in range(len(temp)-1):
			trans_mat[temp[i]][temp[i+1]]+=1
	#print(trans_mat)
	

	for ind in match_final:
		for i in ind:
			emiss_mat[i[1]][i[0]]+=1

	trans_mat = np.asarray(trans_mat, dtype = float)
	emiss_mat = np.asarray(emiss_mat, dtype = float)

	#print(emiss_mat)
	
	#print(trans_mat.shape)
	emiss_mat+=1
	#print(emiss_mat)
	trans_mat+=1
	emiss_mat=emiss_mat/np.sum(emiss_mat,axis=1)[:,np.newaxis]
	trans_mat=trans_mat/np.sum(trans_mat,axis=1)[:,np.newaxis]
		
	#trans_mat=trans_mat/np.sum(trans_mat,axis=1)
	#emiss_mat=emiss_mat/np.sum(emiss_mat,axis=1)
	#print(trans_mat)


	return p_mat,trans_mat,emiss_mat

def write1(p_mat,trans_mat,emiss_mat,prior,emission,transmission):

	with open(prior, mode='w') as output1:

		for i in p_mat:
			output1.write(str(np.float64(i)))
			output1.write('\n')
	with open(transmission, mode='w') as output2:

		for i in trans_mat:
			for x in i:

			
				output2.write(str(np.float64(x)))
				output2.write(' ')

			output2.write('\n')
				
			
	with open(emission, mode='w') as output3:

		for i in emiss_mat:
			for x in i:

			

				output3.write(str(np.float64(x)))
				output3.write(' ')
			output3.write('\n')
				
				


	





	

if __name__=="__main__":
	input1=sys.argv[1]
	word=sys.argv[2]
	tag=sys.argv[3]
	prior=sys.argv[4]
	emission=sys.argv[5]
	transmission=sys.argv[6]
	p_mat,trans_mat,emiss_mat=compute_para(input1,word,tag)
	write1(p_mat,trans_mat,emiss_mat, prior,emission,transmission)


