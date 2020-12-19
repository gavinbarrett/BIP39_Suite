import React from 'react';
import { Link } from 'react-router-dom';
import { Button } from './Button';
import './sass/SideBar.scss';

const SideBar = () => {
	const generate = './static/ui/components/icons/open-iconic-master/beaker.svg';
	const recover = './static/ui/components/icons/open-iconic-master/loop-circular.svg';
	
	return (<div id="sidebar">
	<Link to={"/"}>
		<Button icon={generate} width="25px" height="25px"/>
	</Link>
	<Link to={"/recover"}>
		<Button icon={recover} width="25px" height="25px"/>
	</Link>
	</div>);
}

export {
	SideBar
}
