import {USERNAME, PASSWORD,TOKEN} from './login_info';
const axios = require('axios');
const vis = require('vis');

var git = document.getElementById("git");
var btn = document.getElementById("btn");
var btn2 = document.getElementById("btn2");

var followers = [];
var following = [];

const requisicao = async (followers) => {
	console.log('começando requisições');
	console.log(git.value);
	const api = axios.create({
		baseURL: 'https://api.github.com/users/' + git.value + '/followers',
		headers: {
			'Authorization': {
				username: USERNAME,
				password: PASSWORD
			}
		}
	});

	// Requisição pra pegar a lista inicial de githubs a ser usada
	var response = await api.get('https://api.github.com/users/' + git.value + '/following', {
		auth: {
			username: USERNAME,
			password: PASSWORD,
			token: TOKEN
		}
	})
	.then((response) => {
		var aux = response.data;
		aux.forEach(function (item, index) {
			followers.push({ 
				id: index, 
				shape:'image', 
				image: response.data[index].avatar_url, 
				label: response.data[index].login }
			);
		});
	});

	//Fof é a matriz de seguidores de cada usuário da lista, de acordo com o seu id
	var fof = [];

	// Requisição para a lista de seguidores de cada usuário da lista
	for (const item in followers) {
		var response2 =  await api.get('https://api.github.com/users/' + followers[item].label+ '/followers', {
			auth: {
				username: USERNAME,
				password: PASSWORD,
				token: TOKEN
			}
		})
		.then((response2) => {
			var listUsers = [];
			response2.data.forEach((item,index2) =>{
				listUsers.push(item.login);
			})
			fof.push(listUsers);
		})
	}

	// Preenche o vetor following a partir do fof e do followers
    console.log(followers.length)
	for(var i = 0 ; i < followers.length; i++){
		for(var j = 0; j< fof[i].length; j++){
			for(var k = 0; k< followers.length; k++){
				if(fof[i][j] == followers[k].label){
					following.push({from: i, to: k});
				}
			}
		}				
	}
}

document.addEventListener('DOMContentLoaded', function () {
	btn2.classList.add('hide')	
	var container = document.querySelector('#graph');

	var data = {
		nodes: [],
		edges: []
	}

	var options = {
		nodes: {
			borderWidth: 0,
			size: 42,
			color: {
				border: '#222',
				background: 'transparent'
			},
			font: {
				color: '#111',
				face: 'Helvetica',
				size: 20,
				strokeWidth: 0,
				strokeColor: '#222'
			}
		},
		edges: {
			arrows: {
				to:     {enabled: false, scaleFactor:1, type:'arrow'},
				middle: {enabled: false, scaleFactor:1, type:'arrow'},
				from:   {enabled: true, scaleFactor:1, type:'arrow'}
				},
			color: {
				color: '#CCC',
				highlight: '#A22'
			},
			width: 3,
			length: 500,
			hoverWidth: .05
		}
	}

	var network = new vis.Network(container, data, options);
	async function generateGraph(){
		await requisicao(followers).then(async(api) => {
			git.value = '';
			console.log('requisições feitas')
			data = {
				nodes: followers,
				edges: following
			}
			await network.setData(data);
			await btn.setAttribute('disabled', 'disabled');
			await btn.classList.add('hide')
			await btn2.classList.add('show')	
		});
	}
	async function clear(){
		var select = followers.find(x => x.label ===git.value)
		if (select === undefined){
			alert('Usuário não encontrado!')
		}else{
			network.selectNodes([select.id])
		}
	}

	function cria(){
		data = {
			nodes: [],
			edges: []
		}
		network = new vis.Network(container, data, options);
	}
	btn.onclick = generateGraph;
	btn2.onclick = clear;
	
});
