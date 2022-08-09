from datetime import datetime,date 
from flask import *
from database import *
import uuid
import json
from web3 import Web3, HTTPProvider

# truffle development blockchain address
blockchain_address = 'http://127.0.0.1:9545'
# Client instance to interact with the blockchain
web3 = Web3(HTTPProvider(blockchain_address))
# Set the default account (so we don't need to set the "from" for every transaction call)
web3.eth.defaultAccount = web3.eth.accounts[0]
compiled_contract_path = 'E:/MCA/MCA S4/Main Project/Insurance management/INSURANCE_MANAGEMENT/INSURANCE_MANAGEMENT/node_modules/.bin/build/contracts/insurance.json'
# Deployed contract address (see `migrate` command output: `contract address`)
deployed_contract_address = '0x1C0Dec5A5E03b47d0712c73aD78189994158f47e'
syspath=r"E:\MCA\MCA S4\Main Project\Insurance management\INSURANCE_MANAGEMENT\INSURANCE_MANAGEMENT\static\\"
public=Blueprint('public',__name__)

@public.route('/')
def home():
	return render_template('index.html')


@public.route('/about')
def about():
	return render_template('about.html')


@public.route('/login',methods=['get','post'])
def login():
	if "login" in request.form:
		uname=request.form['un']
		pwd=request.form['pa']
		q="select * from login where username='%s' and password='%s'"%(uname,pwd)
		res=select(q)
		print(res)
		if res:
			if res[0]['usertype']=="admin":
				flash("login successfully")
				return redirect(url_for('admin.adminhome'))


			# elif res[0]['usertype']=="agent":
			# 	q1="select * from agent where login_id='%s'"%(res[0]['login_id'])
			# 	res1=select(q1)
			# 	session['agent_id']=res1[0]['agent_id']
			# 	flash("login successfully")
			# 	return redirect(url_for('agent.agenthome'))

			elif res[0]['usertype']=="client":
				q1="select * from user where login_id='%s'"%(res[0]['login_id'])
				res1=select(q1)
				session['userid']=res1[0]['user_id']
				session['unam']=res1[0]['fname']+" "+res1[0]['lname']
				session['propic']=res1[0]['profile']
				flash("login successfully")
				return redirect(url_for('user.userhome'))

			
	return render_template('login.html')




@public.route('/clientregister',methods=['get','post'])
def clientregister():
	data = {}
	today = date.today()
	data['today'] = today
	if "register" in request.form:
		fna=request.form['f']
		lna=request.form['l']
		s=request.form['s']
		pla=request.form['pl']
		em=request.form['e']
		a=request.form['a']
		hn=request.form['hn']
		i=request.files['i']
		path="static/profile"+str(uuid.uuid4())+i.filename
		i.save(path)
		ii=request.files['ii']
		path1="static/id_proof"+str(uuid.uuid4())+ii.filename
		ii.save(path1)
		uname=request.form['u']
		pwd=request.form['password']
		ql="insert into login values(null,'%s','%s','client')"%(uname,pwd)
		rl=insert(ql)
		qs="insert into user values(null,'%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')"%(rl,fna,lna,pla,s,em,a,hn,path,path1)
		insert(qs)
		with open(compiled_contract_path) as file:
			contract_json = json.load(file)  # load contract info as JSON
			contract_abi = contract_json['abi']  # fetch contract's abi - necessary to call its functions
		contract = web3.eth.contract(address=deployed_contract_address, abi=contract_abi)
		id=web3.eth.get_block_number()
		message = contract.functions.add_client(int(id),rl,fna,lna,a,path1).transact()
		flash("register successfully")
		return redirect(url_for('public.clientregister'))
		
	return render_template('clientregister.html', data = data)