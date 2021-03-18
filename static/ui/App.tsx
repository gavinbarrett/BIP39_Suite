import * as React from 'react';
import * as ReactDOM from 'react-dom';
import * as Router from 'react-router-dom';
import { ScrollToTop } from './components/ScrollToTop';
import { Header } from './components/Header';
import { AppContainer } from './components/AppContainer';
import { Footer } from './components/Footer';
import './components/sass/App.scss';

const App = () => {
	return (<div className="app-wrapper">
		<ScrollToTop/>
		<Header/>
		<AppContainer/>
		<Footer/>
	</div>);
}

ReactDOM.render(<Router.HashRouter><App/></Router.HashRouter>, document.getElementById('root'));
