import * as React from 'react';
import * as Router from 'react-router-dom';
import { BIPGenerator } from './BIPGenerator';
import { Recover } from './Recover';
import './sass/AppContainer.scss';

export const AppContainer = () => {
	const loc = Router.useLocation();
	return (<div className="appcontainer">
		<div id="title">
			{(loc.pathname === '/') ? 'BIP Suite:Generate' : 'BIP Suite:Recover'}
		</div>
		<Router.Switch>
			<Router.Route path='/' exact render={() => <BIPGenerator/>}/>
			<Router.Route path='/recover' render={() => <Recover/>}/>
		</Router.Switch>
	</div>);
}
