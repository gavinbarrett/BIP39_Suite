import * as React from 'react';
import './sass/Documentation.scss';

const DocumentationHeader = () => {
	return (<div className="doc-header">
		{"Documentation"}
	</div>);
}

export const Documentation = () => {
	return (<div className="documentation">
		<DocumentationHeader/>
		<div id="tutorial" className="doc-title">{"Setting up a simple wallet"}</div>
			<div className="doc">
				{"To set up a simple BIP wallet, all you need to do is call the constructor."}
			</div>
		<div id="bippath" className="doc-title">{"Deriving a BIP 44 path"}</div>
			<div className="doc">
				{"To set up a simple BIP wallet, all you need to do is call the constructor."}
			</div>
		<div id="masternode" className="doc-title">{"Deriving the master node"}</div>
			<div className="doc">
			</div>
		<div id="masterkeys" className="doc-title">{"Deriving the master keypair"}</div>
			<div className="doc">
			</div>
		<div id="childkeys" className="doc-title">{"Deriving child keys"}</div>
			<div className="doc">
			</div>
		<div id="addresses" className="doc-title">{"Generating addresses"}</div>
			<div className="doc">
			</div>
	</div>);
}
