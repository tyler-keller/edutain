<script>
    import GoogleButton from '$lib/components/GoogleButton.svelte';
    import { auth, user } from '$lib/firebase';

    import { GoogleAuthProvider, signInWithPopup, signOut } from 'firebase/auth';

    async function  signInWithGoogle() {
        const provider = new GoogleAuthProvider();
        try {
            const result = await signInWithPopup(auth, provider);
            console.log(result);
        } catch (error) {
            console.error(error);
        }
    }
</script>

<h2 class="text-center text-2xl p-6 font-bold">Login</h2>

{#if $user}
    <div class="flex justify-center">
        <button class="p-4 bg-red-500 text-white dark:bg-slate-100 dark:text-black rounded-lg " on:click={() => signOut(auth)}>Sign out</button>
    </div>
{:else}
    <a on:click={signInWithGoogle} href="/login">
        <GoogleButton />
    </a>
{/if}