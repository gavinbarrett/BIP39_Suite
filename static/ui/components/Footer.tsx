import * as React from 'react';
import * as Router from 'react-router-dom';
import './sass/Footer.scss';

export const Footer = () => {
	return (<footer>
		<div className="footer-box">
			<div className="footer-field">
				<Router.Link className="footer-link" to="/">Home</Router.Link>
			</div>
			<div className="footer-field">
				<Router.Link className="footer-link" to="/generate">Generate</Router.Link>
			</div>
			<div className="footer-field">
				<Router.Link className="footer-link" to="/recover">Recover</Router.Link>
			</div>
			<div className="footer-field">
				<Router.Link className="footer-link" to="/download">Download</Router.Link>
			</div>
		</div>
		<div className="footer-box">
			<div className="footer-field">
				<Router.Link className="footer-link" to="/documentation">Documentation</Router.Link>
			</div>
			<a className="footer-field footer-link" href="https://github.com/gavinbarrett/BIP39_Suite">
				Source Code
			</a>
			<div className="footer-field">
				<Router.Link className="footer-link" to="/privacy">Privacy Policy</Router.Link>
			</div>
			<div className="footer-field">
				BipSuite &copy; 2021
			</div>
		</div>
	</footer>);
}
