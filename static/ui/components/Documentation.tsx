import * as React from 'react';
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
	const seed = "seed = '1b7a95e4ee67157b6d369add2dddd2152a5182ba112f882395ec6648efe36fb7a60bb6c4587210fdaca4cef2aa1de06c20f2468eca196beb34bf73fbe652d88f'";
	const wallet = "wallet = BIP32_Account(seed)";
	const xkeys = "xprv, xpub = wallet.gen_master_xkeys(wallet.rootseed)";
	const depth = "depth = 2**31";
	const index = "index = 1";
	const child = "xprv, xpub = wallet.gen_child_xkeys(xprv, xpub, depth, index)";
	const path = "m/44'/0'/0'/0";
	const bippath = "keypairs = wallet.gen_bip44_path.(path)";
	return (<div className="documentation">
		<DocumentationHeader/>
		<div id="tutorial" className="doc-title">{"Setting up a simple wallet"}</div>
			<div className="doc">
				<div className="doc-text">
					<div className="document-text">{"To set up a simple BIP wallet, all you need to do is call the BIP32_Account constructor."}</div>
					<CodeBox code_lines={[impt, seed, wallet]}/>
				</div>
			</div>
		<div id="bippath" className="doc-title">{"Deriving a BIP 44 path"}</div>
			<div className="doc">
				<div className="doc-text">
					<div className="document-text">{"To derive a BIP 44 path, you can use the generate_bip44_path method defined on the BIP32_Account class."}</div>
					<CodeBox code_lines={[path, bippath]}/>
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
				</div>
			</div>
	</div>);
}
