import React from 'react';
import ReactDOM from 'react-dom';
import { HashRouter as Router } from 'react-router-dom';
import { SideBar } from './components/SideBar';
import { AppContainer } from './components/AppContainer';
import './components/sass/App.scss';

const App = () => {
	return (<div className="app">
		<SideBar/>
		<AppContainer/>
	</div>);
}

ReactDOM.render(<Router><App/></Router>, document.getElementById('root'));
