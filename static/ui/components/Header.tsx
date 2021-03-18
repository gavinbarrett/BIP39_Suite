import * as React from 'react';
import * as Router from 'react-router-dom';
import './sass/Header.scss';

const Navigator = () => {
	return (<nav>
		<Router.Link to="/">Home</Router.Link>
		<Router.Link to="/generate">Generate</Router.Link>
		<Router.Link to="/recover">Recover</Router.Link>
		<Router.Link to="/download">Download</Router.Link>
		<Router.Link to="/documentation">Docs</Router.Link>
	</nav>);
}

export const Header = () => {
	return (<header>
		<div id="header-text">{"biptools"}</div>
		<Navigator/>
	</header>);
}
