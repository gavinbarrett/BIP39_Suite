import * as React from 'react';
import { SideBar } from './SideBar';
import './sass/Documentation.scss';

const DocumentationHeader = () => {
	return (<div className="doc-header">
		{"BipPy Documentation"}
	</div>);
}

const CodeBox = ({code_lines}) => {
	return (<div className="code-box">
		{code_lines.map((elem, index) => {
			return <code className={`code-line`}>{elem}</code>
		})}
	</div>);
}

export const Documentation = () => {
	const impt = "from bippy import BIP32_Account"
	const seed = "seed = '000102030405060708090a0b0c0d0e0f'";
	const wallet = "wallet = BIP32_Account(seed)";
	const xkeys = "xprv, xpub = wallet.gen_master_xkeys(wallet.rootseed)";
	const depth = "depth = 2**31";
	const index = "index = 1";
	const child = "xprv, xpub = wallet.gen_child_xkeys(xprv, xpub, depth, index)";
	const path = "m/44'/0'/0'/0";
	const bippath = "keypairs = wallet.gen_bip44_path.(path)";
	return (<div className="app"><SideBar/>
	<div className="documentation">
		<DocumentationHeader/>
		<div id="tutorial" className="doc-title">{"Setting up a simple wallet"}</div>
			<div className="doc">
				<div className="doc-text">
					<div className="document-text">{"To set up a simple BIP wallet, all you need to do is call the BIP32_Account constructor and pass in the seed phrase."}</div>
					<CodeBox code_lines={[impt, seed, wallet]}/>
				</div>
			</div>
		<div id="bippath" className="doc-title">{"Deriving a BIP 44 path"}</div>
			<div className="doc">
				<div className="doc-text">
					<div className="document-text">{"To derive a BIP 44 path, you can use the gen_bip44_path method defined on the BIP32_Account class."}</div>
					<CodeBox code_lines={[path, bippath]}/>
					{"This will return a list of keys derived along the given path."}
				</div>
			</div>
		<div id="masternode" className="doc-title">{"Deriving the master node"}</div>
			<div className="doc">
				<div className="doc-text">
					{"To discover the master node associated with the BIP32 account, use the generate_rootkey method."}
					<CodeBox code_lines={["rootkey = wallet.generate_rootkey(seed)"]}/>
				</div>
			</div>
		<div id="masterkeys" className="doc-title">{"Deriving the master keypair"}</div>
			<div className="doc">
				<div className="doc-text">
					{"The master key pair associated with the mnemonic and master node can be derived with the gen_master_xkeys method."}
					<CodeBox code_lines={[xkeys]}/>
				</div>
			</div>
		<div id="childkeys" className="doc-title">{"Deriving child keys"}</div>
			<div className="doc">
				<div className="doc-text">
					{"Child keys can be derived by calling the gen_child_xkeys method. Be sure to only use depths in the range 0-255 and indices from 0 - 2^31 - 1 for unhardened keys and 2^31 - 2^32 for hardened keys."}
					<CodeBox code_lines={[index, depth, child]}/>
				</div>
			</div>
		<div id="addresses" className="doc-title">{"Generating addresses"}</div>
			<div className="doc">
				<div className="doc-text">
					{"Legacy (P2PKH) Bitcoin addresses can be computed with the gen_legacy_addr function on any extended public key."}
					<CodeBox code_lines={["addr = wallet.gen_legacy_addr(xpub)"]}/>
					{"P2SH-P2WPKH addresses can be computed with the gen_segwit_addr"}
				</div>
			</div>
	</div></div>);
}
