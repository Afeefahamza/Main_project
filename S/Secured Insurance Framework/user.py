from public import *
from datetime import date,datetime

user=Blueprint('user',__name__)


# truffle development blockchain address
blockchain_address = 'http://127.0.0.1:9545'
# Client instance to interact with the blockchain
web3 = Web3(HTTPProvider(blockchain_address))
# Set the default account (so we don't need to set the "from" for every transaction call)
web3.eth.defaultAccount = web3.eth.accounts[0]
compiled_contract_path = 'E:/MCA/MCA S4/Main Project/Insurance management/INSURANCE_MANAGEMENT/INSURANCE_MANAGEMENT/node_modules/.bin/build/contracts/insurance.json'
# Deployed contract address (see `migrate` command output: `contract address`)
deployed_contract_address = '0x1C0Dec5A5E03b47d0712c73aD78189994158f47e'
# deployed_contract_address = '0x3534a9a1Eff73497f1822f963AAcA4F36ef5ffe9'





@user.route('/userhome')
def userhome():
	data={}
	data['pic']=session['propic']
	data['username']=session['unam']
	q="select * from user where user_id='%s'"%(session['userid'])
	data['u']=select(q)
	return render_template("userhome.html",data=data)




@user.route('/userviewpolicy',methods=['get','post'])
def userviewpolicy():
	data={}

	q="select * from policy "
	r=select(q)
	data['pdt']=r
	if "action" in request.args:
		action=request.args['action']
		policy_id=request.args['policy_id']
	else:
		action=None
	if action=="request":
		q1="select * from request where policy_id='%s' and user_id='%s'"%(policy_id,session['userid'])
		print('llllllllllll',q1)
		res1=select(q1)
		
		if res1:
			flash(" Already Appiled")
			return redirect(url_for('user.userviewpolicy'))		
		else:
	
			q="insert into request values(null,'%s','%s',curdate(),'pending')"%(policy_id,session['userid'])
			r=insert(q)
			flash("requested successfully")
			return redirect(url_for('user.userviewrequest'))
	return render_template('userviewpolicy.html',data=data)






@user.route('/usersendcomplaint',methods=['get','post'])
def usersendcomplaint():
	data={}
	data['pic']=session['propic']
	data['username']=session['unam']
	user_id=session['userid']

	q="select * from complaint where user_id='%s'"%(user_id)
	r=select(q)
	data['comp']=r
	if "send" in request.form:
		complaint=request.form['com']
		sid=session['userid']
		q="insert into complaint values(null,'%s','%s','reply-pending',curdate())"%(sid,complaint)
		insert(q)
		flash("send successfully")
		return redirect(url_for('user.usersendcomplaint'))
	return render_template('usersendcomplaint.html',data=data)
@user.route('/userviewrequest',methods=['get','post'])
def userviewrequest():
	data={}
	user_id=session['userid']
	q="select * from request inner join policy using(policy_id)where user_id='%s'"%(user_id)
	r1=select(q)
	data['user']=r1
	
	return render_template('userviewrequest.html',data=data)


@user.route('/usermakepayment',methods=['get','post'])
def usermakepayment():
	data={}
	premium=request.args['premium']
	policy_id=request.args['policy_id']
	session['policy_id']=policy_id
	data['premium']=premium
# //////////////////////////////////////////////////////

	with open(compiled_contract_path) as file:
		contract_json = json.load(file)  # load contract info as JSON
		contract_abi = contract_json['abi']  # fetch contract's abi - necessary to call its functions
	contract = web3.eth.contract(address=deployed_contract_address, abi=contract_abi)
	blocknumber = web3.eth.get_block_number()
	res = []
	try:
		for i in range(blocknumber, 0, -1):
			a = web3.eth.get_transaction_by_block(i, 0)
			decoded_input = contract.decode_function_input(a['input'])
			print(decoded_input)
			if str(decoded_input[0]) == "<Function add_payment(uint256,uint256,uint256,string,string)>":
				if int(decoded_input[1]['u_id']) == int(session['userid']) and int(decoded_input[1]['p_id']) == int(session['policy_id']):
					res.append(decoded_input[1])
	except Exception as e:
		print("", e)
	data['view']=res
	print(res)

	l1=len(res)
	# print(res[l1-1]['date'])
	if res:
		pdate="SELECT MONTH('%s') as m"%(res[0]['date'])
		print('pppppppppp',pdate)
		ppdate=select(pdate)
		mnth="SELECT MONTH(CURDATE()) as m"
		print('mmmmmmmm',mnth)
		mmnth=select(mnth)
		if ppdate==mmnth:
			flash('Already paid')
			return redirect(url_for('user.userhome'))
		

		elif ppdate!=mmnth:
			result=int(mmnth[0]['m'])-int(ppdate[0]['m'])
			print('kkkkkk',result)
			amt=int(result)*int(premium)
			print('kkkkkk',result)
			data['premium']=amt
			print('ddddddddd',data['premium'])

		else:
			data['premium']=premium
# 	else:
# 		data['premium']=premium

# # //////////////////////////////////////////////////////
	if 'payment' in request.form:
		premium=request.args['premium']
		# data['premium_amt']=premium
		policy_id=request.args['policy_id']
		a=request.form['a']
		import  datetime
		d=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
		# d="2022-06-11"
		with open(compiled_contract_path) as file:
			contract_json = json.load(file)  # load contract info as JSON
			contract_abi = contract_json['abi']  # fetch contract's abi - necessary to call its functions
		contract = web3.eth.contract(address=deployed_contract_address, abi=contract_abi)
		id=web3.eth.get_block_number()
		message = contract.functions.add_payment(int(id),int(session['userid']),int(policy_id),a,d).transact()
		flash("payment successfully")
		return redirect(url_for('user.userhome'))

	
	return render_template("usermakepayment.html",data=data)





@user.route('/userviewpayment',methods=['get','post'])
def userviewpayment():
	data={}


	with open(compiled_contract_path) as file:
		contract_json = json.load(file)  # load contract info as JSON
		contract_abi = contract_json['abi']  # fetch contract's abi - necessary to call its functions
	contract = web3.eth.contract(address=deployed_contract_address, abi=contract_abi)
	blocknumber = web3.eth.get_block_number()
	res = []
	try:
		for i in range(blocknumber, 0, -1):
			a = web3.eth.get_transaction_by_block(i, 0)
			decoded_input = contract.decode_function_input(a['input'])
			print(decoded_input)
			if str(decoded_input[0]) == "<Function add_payment(uint256,uint256,uint256,string,string)>":
				if int(decoded_input[1]['u_id']) == int(session['userid']):
					res.append(decoded_input[1])
	except Exception as e:
		print("", e)
	data['view']=res

	if res:
		q1="select * from policy where policy_id='%s'"%(res[0]['p_id'])
		print(q1)
		res1=select(q1)
		data['pname']=res1[0]['policy']
		print(res1[0]['policy'])

	return render_template("userviewpayment.html",data=data)


@user.route('/generatedoc')
def generatedoc():
	data={}
	today=date.today()
	print(today)
	data['today']=today
	now=datetime.now()
	current_time=now.strftime("%H:%M:%S")
	print(current_time)
	data['current_time']=current_time	
	
	with open(compiled_contract_path) as file:
		contract_json = json.load(file)  # load contract info as JSON
		contract_abi = contract_json['abi']  # fetch contract's abi - necessary to call its functions
	contract = web3.eth.contract(address=deployed_contract_address, abi=contract_abi)
	blocknumber = web3.eth.get_block_number()
	res = []
	try:
		for i in range(blocknumber, 0, -1):
			a = web3.eth.get_transaction_by_block(i, 0)
			decoded_input = contract.decode_function_input(a['input'])
			print(decoded_input)
			if str(decoded_input[0]) == "<Function add_payment(uint256,uint256,uint256,string,string)>":
				if int(decoded_input[1]['u_id']) == int(session['userid']):
					res.append(decoded_input[1])
	except Exception as e:
		print("", e)
	data['view']=res

	q1="select * from user  where user_id='%s'"%(res[0]['u_id'])
	res1=select(q1)
	data['uname']=res1[0]['fname']
	data['ph']=res1[0]['phone']
	q2="select * from policy  where policy_id='%s'"%(res[0]['p_id'])
	res2=select(q2)
	data['pol']=res2[0]['policy']
	return render_template('generatedoc.html',data=data)



@user.route('/userclaimpolicy',methods=['get','post'])
def userclaimpolicy():
	data={}
	q="select * from policy"
	data['pol']=select(q)
	if "register" in request.form:
		policy_id=request.form['pol']
		i=request.files['i']
		path="static/certificate/"+str(uuid.uuid4())+i.filename
		i.save(path)
		iii=request.files['iii']
		path2="static/document_policy/"+str(uuid.uuid4())+iii.filename
		iii.save(path2)
		ii=request.files['ii']
		path1="static/id_proof/"+str(uuid.uuid4())+ii.filename
		ii.save(path1)

		ql="insert into claim values(null,'%s','%s','%s','%s','%s','pending')"%(policy_id,session['userid'],path,path2,path1)
		rl=insert(ql)
		
		flash("uploaded successfully")
		return redirect(url_for('user.userclaimpolicy',policy_id=policy_id))
		
	return render_template('userclaimpolicy.html',data=data)




@user.route('/userview_claim',methods=['get','post'])
def userview_claim():
	data={}
	q="select * from claim inner join policy using(policy_id) where user_id='%s' "%(session['userid'])
	r=select(q)
	data['user']=r
	
	return render_template('userviewclaim.html',data=data)

