import * as React from 'react';
import { Prompt } from './Prompt';
import { SideBar } from './SideBar';
import { SeedContainer } from './SeedContainer';
import { PathSelector } from './PathSelector';
import './sass/Recover.scss';

export const Recover = () => {
	const [mnemonics, updateMnemonics] = React.useState('');
	const [salt, updateSalt] = React.useState('');
	const [rootseed, updateRootseed] = React.useState('');
	const [xprv, updateXprv] = React.useState('');
	const [xpub, updateXpub] = React.useState('');
	const [hideMnemonic, updateHideMnemonic] = React.useState('password');
	const [hidePass, updateHidePass] = React.useState('password');
	const [eyeMnemonic, updateEyeMnemonic] = React.useState('hidden');
	const [eyePass, updateEyePass] = React.useState('hidden');
	const [path, updatePath] = React.useState("Native SegWit");

	const prompt1 = 'Enter your BIP32 mnemonic seed phrase, and your password if your wallet has one.';
	const prompt2 = 'Select whether you want to see keys for Legacy, SegWit, or Native SegWit addresses.';

	const validMnemonics = (mnemonics) => {
		if (mnemonics === "") return false;
		return true;
	}

	const recover_seed = async () => {
		if (!validMnemonics(mnemonics)) return;
		const resp = await fetch('/recover', {method: "POST", body: JSON.stringify({"mnemonics": mnemonics, "salt": salt})});
		const data = await resp.json();
		if (data && data["seed"]) {
			// update container properties
			updateRootseed(data["seed"]);
			updateXprv(data["m_xprv"]);
			updateXpub(data["m_xpub"]);
		}
	}
	
	const update_seed = event => {
		updateMnemonics(event.target.value);
		if (event.target.value === "" && hideMnemonic !== "password") {
			updateHideMnemonic("password")
			updateEyeMnemonic("hidden");
		}
	}
	
	const update_salt = event => {
		updateSalt(event.target.value);
		if (event.target.value === "" && hidePass !== "password") {
			updateHidePass("password")
			updateEyePass("hidden");
		}
	}

	const update_mnemonic_box = () => {
		if (mnemonics === "") return;
		if (hideMnemonic === "password") {
			updateHideMnemonic("text");
			updateEyeMnemonic("displayed");
		} else {
			updateHideMnemonic("password");
			updateEyeMnemonic("hidden");
		}
	}

	const update_pass_box = () => {
		if (salt === "") return;
		if (hidePass === "password") {
			updateHidePass("text")
			updateEyePass("displayed");
		} else {
			updateHidePass("password")
			updateEyePass("hidden");
		}
	}

	return (<div className="recovery-app">
	<SideBar/>
	<div className="recovery-box">
	<div className="recovery-input">
		<div className="recovery-line">
			<input type={hideMnemonic} pattern={'([a-z]+\s?){12,24}'} placeholder="Enter mnemonic seed phrase here" title="Mnemonic Seed" onChange={update_seed} autoComplete={"off"}/><div className={`password-hider ${eyeMnemonic}`} onClick={update_mnemonic_box}></div>
		</div>
		<div className="recovery-line">
			<input type={hidePass} placeholder="Enter your HD wallet passphrase here" title="Salting Phrase" onChange={update_salt} autoComplete={"off"}/><div className={`password-hider ${eyePass}`} onClick={update_pass_box}></div>
		</div>
			<PathSelector path={path} updatePath={updatePath}/>
			<div className="recovery-wrapper">
				<button className="recovery-button" onClick={recover_seed}>Recover</button>
			</div>
		</div><div className="recovery-seed">
			{rootseed ? <SeedContainer phrase={mnemonics} seed={rootseed} m_xprv={xprv} m_xpub={xpub}/> : <Prompt texts={[prompt1, prompt2]}/>}
		</div>
	</div></div>);
}
