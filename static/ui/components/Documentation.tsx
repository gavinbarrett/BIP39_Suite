import * as React from 'react';
import { SideBar } from './SideBar';
import './sass/Documentation.scss';

const DocumentationHeader = () => {
	return (<div className="doc-header">
		{"biptools Documentation"}
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
	const impt = "from biptools import BIP49"
	const mnemonic = "mnemonic = 'twelve pride tower pass fruit ozone exclude lemon pool wall abandon want answer vapor chunk'"
	const seed = "seed = '000102030405060708090a0b0c0d0e0f'";
	const bipseed = "seed = '367d8b708d8b3c0bb23b75456e95b17dff49ab0332d84c8bf6a843a62dc778fb12e3e05cd32873f4eac1ee49fa9a8796ae1c9beb2983942a6dd38b58dbd2f075'"
	const wallet_49_1 = "wallet_49 = BIP49(mnemonic)";
	const wallet_49_2 = "wallet_49 = BIP49(seed, True)";
	const ykeys = "yprv, ypub = wallet_49.get_master_keys()";
	const path = "m/44'/0'/0'/0";
	const bippath = "keypairs = wallet.gen_bip44_path.(path)";
	return (<div className="app"><SideBar/>
	<div className="documentation">
		<DocumentationHeader/>
		<div id="tutorial" className="doc-title">{"Setting up a wallet"}</div>
			<div className="doc">
				<div className="doc-text">
					<div className="document-text">{"To set up a BIP compatible wallet, you need to call one of the BIP44/49/84 constructors. Two constructor APIs exist, the first allows the user to pass in a BIP39 mnemonic string and another where the user can pass a BIP39 seed with an additional boolean argument set to True. Both methods are demonstrated below"}</div>
					<CodeBox code_lines={[impt, mnemonic, bipseed, wallet_49_1, wallet_49_2]}/>
				</div>
			</div>
		<div id="masterkeys" className="doc-title">{"Getting the master keypair"}</div>
			<div className="doc">
				<div className="doc-text">
					{"The master key pair associated with the wallet can be retrieved with the get_master_keys() method."}
					<CodeBox code_lines={[ykeys]}/>
				</div>
			</div>
		{/*<div id="bippath" className="doc-title">{"Deriving a BIP 44 path"}</div>
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
			</div>*/}
		{/*<div id="childkeys" className="doc-title">{"Deriving child keys"}</div>
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
			</div>*/}
	</div></div>);
}
