import React from 'react';
import { Route, Switch, useLocation } from 'react-router-dom';
import { Generator } from './Generator';
import { Recover } from './Recover';
import './sass/AppContainer.scss';

const AppContainer = () => {

	const loc = useLocation();
	
	return (<div className="appcontainer">
		<div id="title">
			{(loc.pathname === '/') ? 'BIP Suite:Generate' : 'BIP Suite:Recover'}
		</div>
		<Switch>
			<Route path='/' exact render={() => <Generator/>}/>
			<Route path='/recover' render={() => <Recover/>}/>
		</Switch>
	</div>);
}

export {
	AppContainer
}
