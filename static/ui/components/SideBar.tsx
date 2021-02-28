import * as React from 'react';
import * as Router from 'react-router-dom';
import { Button } from './Button';
import './sass/SideBar.scss';

export const SideBar = () => {
	const key = './static/ui/components/icons/open-iconic-master/key.svg';
	const generate = './static/ui/components/icons/open-iconic-master/beaker.svg';
	const recover = './static/ui/components/icons/open-iconic-master/loop-circular.svg';
	const download = './static/ui/components/icons/open-iconic-master/download.svg';
	const documentation = './static/ui/components/icons/open-iconic-master/document.svg';

	return (<div id="sidebar">
	<Router.Link to={"/"}>
		<Button icon={key} title={"biptools"}/>
	</Router.Link>
	<Router.Link to={"/generate"}>
		<Button icon={generate} title={"Generate Wallet"}/>
	</Router.Link>
	<Router.Link to={"/recover"}>
		<Button icon={recover} title={"Recover Wallet"}/>
	</Router.Link>
	<Router.Link to={"/download"}>
		<Button icon={download} title={"Download Client"}/>
	</Router.Link>
	<Router.Link to={"/documentation"}>
		<Button icon={documentation} title={"Documentation"}/>
	</Router.Link>
	</div>);
}
