import numpy as np
import sys

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
	#get indices and tags index in matrix
	match_final=[]
	for i in input3:
		match=[]
		current=i
		current1=current.split(' ')
		#print(len(current1))

		for x in current1:
			y=1
			word,tag=x.split('_')
			tag_index=tag3.index(tag)
			word_index=word3.index(word)
			match.append([word_index,tag_index])
		match_final.append(match)

	return match_final,word_len, tag_len, word3, tag3

def load_mat(prior,emiss,trans):
	prior=np.loadtxt(prior)
	emiss=np.loadtxt(emiss)
	trans=np.loadtxt(trans)
	prior = np.asarray(prior, dtype = float)
	emiss = np.asarray(emiss, dtype = float)
	trans = np.asarray(trans, dtype = float)
	return prior,emiss,trans
def getalpha(row1,word_len,tag_len, prior,emiss,trans):
	alpha=np.zeros((len(row1),tag_len))

	#for k in range(0,tag_len):
		#alpha[0][k]=1.0
	for k in range(0,tag_len):
		alpha[0][k]=emiss[k,row1[0][0]]*prior[k]
	for t in range(1,len(row1)):
		for k in range(0,tag_len):
			sum=0.0
			for i in range(0,tag_len):
				sum+=alpha[t-1,i]*trans[i,k]
				

			alpha[t,k]=emiss[k,[row1[t][0]]]*sum
	alpha_mod=np.log(alpha)
	alpha_all.append(alpha_mod)
	#print(alpha_mod)
	#print("alpha is")
	#print(alpha)
	return alpha

	#print(alpha)
def getbeta(row,word_len,tag_len, prior,emiss,trans):
	beta=np.zeros((len(row),tag_len))
	for i in range(tag_len):
		beta[[len(row)-1],i]=1.0

	for t in range(len(row)-2,-1,-1):
		for k in range(0,tag_len):
			sum=0.0
			for i in range(0,tag_len):
				sum+=emiss[i,row[t+1][0]]*beta[t+1,i]*trans[k,i]
			beta[t,k]=sum
	beta_all.append(np.log(beta))
	beta_mod=np.log(beta)
	#print("beta is new")
	#print(np.log(beta))
	#print(beta)
	return beta


def compute_pred(row, alpha, beta,):
	count=0
	predictionx=[]
	predictiony=[]
	for t in range(len(row)):
		alpha_temp=alpha[t]
		beta_temp=beta[t]
		intermediate=np.argmax(np.multiply(alpha_temp,beta_temp))
		if intermediate==row[t][1]:
			count+=1
		#temp=max(intermediate)
		#temp_list=[]
		#for i in range(len(intermediate)):
			#if intermediate[i]==temp:
				#temp_list.append(i)

		#y_cap=np.argmax(alpha_temp*beta_temp)
		#print("ycap")
		#print(y_cap)
		#print("actual y")
		#print(row[t][1])
		#if row[t][1] in temp_list:
			#count+=1

		predictionx.append([row[t][0],intermediate])
		predictiony.append(intermediate)

	
	#compute log likelihood here
	logl=np.log(np.sum(alpha[len(row)-1,:]))
	return predictionx, predictiony, count,len(row), logl
def write_output(final_ll,accuracy,final_predictions,predict,metric,word_list,tag_list):
	with open(metric, mode='w') as output1:


	
		output1.write("Average Log-Likelihood: ")
		output1.write(str(round(final_ll,8)))
		output1.write('\n')
		output1.write("Accuracy: ")
		output1.write(str(round(accuracy,12)))
	with open(predict, mode='w') as output2:
		for i in final_predictions:
			for x in i:
				output2.write(word_list[x[0]])
				output2.write("_")
				output2.write(tag_list[x[1]])
				output2.write(' ')
			output2.rstrip()
			output2.write('\n')





if __name__ == "__main__":
	test_data=sys.argv[1]
	word=sys.argv[2]
	tag=sys.argv[3]
	prior=sys.argv[4]
	emiss=sys.argv[5]
	trans=sys.argv[6]
	predict=sys.argv[7]
	metric=sys.argv[8]
	alpha_all=[]
	beta_all=[]

	#get the converted testdata, word len and tag len of test data
	test_match,word_len,tag_len,word_list,tag_list=compute_para(test_data,word,tag) 


	#get the list for of prior, emiss and trans matrix
	prior,emiss,trans=load_mat(prior,emiss,trans)
	final_count=[]
	final_total=0.0
	loglikeli=0.0
	final_predictions=[]

	#print(test_match[0])
	for row in test_match:
		alpha=getalpha(row,word_len,tag_len, prior,emiss,trans)
		beta=getbeta(row,word_len,tag_len, prior,emiss,trans)
		predictionx,predictiony,count,total,logl=compute_pred(row, alpha, beta)
		final_total+=total
		final_count.append(count)
		loglikeli+=logl
		final_predictions.append(predictionx)
	final_ll=float(loglikeli)/float(len(test_match))

	#print(alpha)
	accuracy=sum(final_count)/final_total
	
	print(len(final_predictions))
	print(len(test_match))
	write_output(final_ll,accuracy,final_predictions,predict,metric,word_list,tag_list)

	