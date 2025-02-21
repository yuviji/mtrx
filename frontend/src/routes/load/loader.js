/* eslint-disable @typescript-eslint/no-unused-vars */
// eslint-disable-next-line @typescript-eslint/ban-ts-comment
// @ts-expect-error
import Spinner from './Spinner.svelte';

// eslint-disable-next-line @typescript-eslint/ban-ts-comment
// @ts-expect-error
export const loader = (node, loading) => {
	/**
     * @type {{ $destroy: () => void; } | undefined}
     */
	let Spin, loadingValue;
	// eslint-disable-next-line @typescript-eslint/ban-ts-comment
	// @ts-expect-error
	const unsubscribe = loading.subscribe(loading => {
		if(loading){
			Spin = new Spinner({
				target: node,
				intro: true
			})
		} else {
			if(Spin){
				Spin?.$destroy?.()
				Spin = undefined;
			}
		}
	})
}