import * as React from 'react';
import { SideBar } from './SideBar';
import './sass/PrivacyPolicy.scss';

export const PrivacyPolicy = () => {
	return (<div className="privacy-app">
	<SideBar/>
	<div className="privacy-policy">
		{"This is the privacy policy"}
	</div></div>);
}
