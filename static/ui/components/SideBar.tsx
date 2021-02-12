import * as React from 'react';
import * as Router from 'react-router-dom';
import { Button } from './Button';
import './sass/SideBar.scss';

export const SideBar = () => {
	const generate = './static/ui/components/icons/open-iconic-master/beaker.svg';
	const recover = './static/ui/components/icons/open-iconic-master/loop-circular.svg';
	return (<div id="sidebar">
	<Router.Link to={"/"}>
		<Button icon={generate}/>
	</Router.Link>
	<Router.Link to={"/recover"}>
		<Button icon={recover}/>
	</Router.Link>
	</div>);
}
