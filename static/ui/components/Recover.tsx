import * as React from 'react';
import { Prompt } from './Prompt';
import { SeedContainer } from './SeedContainer';
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
	
	const update_seed = event => updateMnemonics(event.target.value)
	
	const update_salt = event => updateSalt(event.target.value);

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

	return (<div className="recovery-box">
	<div className="recovery-input">
		<div className="recovery-line">
			<input type={hideMnemonic} pattern={'([a-z]+\s?){12,24}'} placeholder="Enter mnemonic seed phrase here" title="Mnemonic Seed" onChange={update_seed}/><div className={`password-hider ${eyeMnemonic}`} onClick={update_mnemonic_box}></div>
		</div>
		<div className="recovery-line">
			<input type={hidePass} placeholder="Enter passphrase here" title="Salting Phrase" onChange={update_salt}/><div className={`password-hider ${eyePass}`} onClick={update_pass_box}></div>
		</div>
			<button className="recovery-button" onClick={recover_seed}>Recover</button>
		</div><div className="recovery-seed">
			{rootseed ? <SeedContainer phrase={mnemonics} seed={rootseed} m_xprv={xprv} m_xpub={xpub}/> : <Prompt text={"this is a fucking prompt"}/>}
		</div>
	</div>);
}
