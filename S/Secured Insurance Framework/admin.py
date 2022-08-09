from flask import *
from database import *
import json
from web3 import Web3, HTTPProvider


admin=Blueprint('admin',__name__)




# truffle development blockchain address
blockchain_address = 'http://127.0.0.1:9545'
# Client instance to interact with the blockchain
web3 = Web3(HTTPProvider(blockchain_address))
# Set the default account (so we don't need to set the "from" for every transaction call)
web3.eth.defaultAccount = web3.eth.accounts[0]
compiled_contract_path = 'E:/MCA/MCA S4/Main Project/Insurance management/INSURANCE_MANAGEMENT/INSURANCE_MANAGEMENT/node_modules/.bin/build/contracts/insurance.json'
# Deployed contract address (see `migrate` command output: `contract address`)
deployed_contract_address = '0x1C0Dec5A5E03b47d0712c73aD78189994158f47e'



@admin.route('/adminhome')
def adminhome():
	return render_template('adminhome.html')





@admin.route('/adminviewcomplaintandsendreply',methods=['get','post'])
def adminviewcomplaintandsendreply():
	data={}
	q="SELECT * FROM complaint INNER JOIN user using (user_id)"
	r=select(q)
	data['complaints']=r
	return render_template('adminviewcomplaintandsendreply.html',data=data)

@admin.route('/adminsendreply',methods=['get','post'])
def adminsendreply():
	if "send" in request.form:
		r=request.form['r']
		cid=request.args['cid']
		q="update complaint set reply='%s' where complaint_id='%s'"%(r,cid)
		delete(q)
		flash("send successfully")
		return redirect(url_for('admin.adminviewcomplaintandsendreply'))

	return render_template('adminsendreply.html')






@admin.route('/adminmanagepolicy',methods=['get','post'])
def adminmanagepolicy():
	data={}
	
	if "add" in request.form:
		p=request.form['p']
		d=request.form['d']
		a=request.form['a']
		pr=request.form['pr']
		t=request.form['t']
		
	
	
		qs="insert into policy values(null,'%s','%s','%s','%s','%s')"%(p,d,a,pr,t)
		insert(qs)
		flash("added successfully")
		return redirect(url_for('admin.adminmanagepolicy'))
	if "action" in request.args:
		action=request.args['action']
		pid=request.args['pid']
	else:
		action=None
	if "update" in request.form:
		p=request.form['p']
		d=request.form['d']
		a=request.form['a']
		pr=request.form['pr']
		t=request.form['t']
		q="update policy set policy='%s',category='%s',sum_assured='%s',premium='%s',tenure='%s' where policy_id='%s'"%(p,d,a,pr,t,pid)
		print(q)
		r=update(q)
		flash("update successfully")
		return redirect(url_for('admin.adminmanagepolicy'))
	if action=="update":
		q="select * from  policy where policy_id='%s'"%(pid)
		r=select(q)
		data['updates']=r
	if action=="delete":
		q="delete from policy  where policy_id='%s'"%(pid)
		update(q)
		flash("delete successfully")

		return redirect(url_for('admin.adminmanagepolicy'))
	q="select * from policy "
	r=select(q)
	data['pdt']=r
	return render_template('adminmanagepolicy.html',data=data)





@admin.route('/adminappliedclients',methods=['get','post'])
def adminappliedclients():
	data={}
	q="select * from request inner join user using(user_id)inner join policy using(policy_id) "
	r=select(q)
	data['user']=r
	if "action" in request.args:
		action=request.args['action']
		request_id=request.args['request_id']
	else:
		action=None

	if action=="accept":
		q="update  request set status='accept' where request_id='%s'"%(request_id)
		r=update(q)
		q="SELECT * FROM USER INNER JOIN request USING(user_id) where request_id='%s'"%(request_id)
		print(q)
		res=select(q)
		flash("accept successfully")
		return redirect(url_for('admin.adminappliedclients'))
	if action=="reject":
		q="update  request set status='reject' where request_id='%s'"%(request_id)
		r=update(q)
		flash("reject successfully")
		return redirect(url_for('admin.adminappliedclients'))


	
	return render_template('adminviewpolicyrequested.html',data=data)

@admin.route('/adminview_claim',methods=['get','post'])
def adminview_claim():
	data={}
	q="select * from claim inner join user using(user_id)inner join policy using(policy_id)"
	r=select(q)
	data['user']=r
	if "action" in request.args:
		action=request.args['action']
		claim_id=request.args['claim_id']
		user_id=request.args['user_id']
		policy_id=request.args['policy_id']
	else:
		action=None

	if action=="accept":
		q="update  claim set status='accept' where claim_id='%s'"%(claim_id)
		r=update(q)
		q1="select * from claim where policy_id='%s'"%(claim_id)
		res=select(q1)
		with open(compiled_contract_path) as file:
			contract_json = json.load(file)  # load contract info as JSON
			contract_abi = contract_json['abi']  # fetch contract's abi - necessary to call its functions
		contract = web3.eth.contract(address=deployed_contract_address, abi=contract_abi)
		id=web3.eth.get_block_number()
		message = contract.functions.add_claim(int(id),int(res[0]['user_id']),int(res[0]['policy_id']),res[0]['cert_of_proof'],res[0]['policy_doc'],res[0]['id_proof']).transact()
		flash("added successfully")
		return redirect(url_for('admin.adminview_claim'))
		flash("accept successfully")
		return redirect(url_for('admin.adminview_claim'))
	if action=="reject":
		q="update  claim set status='reject' where claim_id='%s'"%(claim_id)
		r=update(q)
		flash("reject successfully")
		return redirect(url_for('admin.adminview_claim'))

	return render_template('adminview_claim.html',data=data)

@admin.route('/adminviewclient',methods=['get','post'])
def adminviewclient():
	data={}
	q="select * from request inner join user using(user_id)inner join policy using(policy_id) "
	r=select(q)
	data['user']=r
	return render_template('adminviewclient.html',data=data)

@admin.route('/adminviewpayments',methods=['get','post'])
def adminviewpayments():
	data={}

	session['user_id']=request.args['user_id']

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
				# if int(decoded_input[1]['u_id']) == int(session['user_id']):
					res.append(decoded_input[1])
	except Exception as e:
		print("", e)
	data['view']=res


	q1="select * from user  where user_id='%s'"%(session['user_id'])
	res1=select(q1)
	data['uname']=res1[0]['fname']
	q2="select * from policy  where policy_id='%s'"%(res[0]['p_id'])
	res2=select(q2)
	data['pol']=res2[0]['policy']
	return render_template("adminviewpayments.html",data=data)



@admin.route('/adminmakepayment',methods=['get','post'])
def adminmakepayment():
	data={}
	
	if 'payment' in request.form:
		sum_assured=request.args['sum_assured']
		data['sum_assured']=sum_assured
		policy_id=request.args['policy_id']
		user_id=request.args['user_id']
		claim_id=request.args['claim_id']
		q="insert into payment values(null,'%s','%s','%s',curdate())"%(user_id,policy_id,sum_assured)
		insert(q)
		q="update request set status='claimed' where user_id='%s' and  policy_id='%s'"%(user_id,policy_id)
		update(q)
		q="update claim set status='claimed' where claim_id='%s'"%(claim_id)
		update(q)
		flash("payment successfully")
		return redirect(url_for('admin.adminview_claim'))

	
	return render_template("adminmakepayment.html",data=data)
