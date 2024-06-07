<script>
  import { auth, user } from '$lib/firebase';
  import { GoogleAuthProvider, signInWithPopup, signOut } from 'firebase/auth';

  async function signInWithGoogle() {
    const provider = new GoogleAuthProvider();
    try {
      const result = await signInWithPopup(auth, provider);
      console.log(result);
    } catch (error) {
      console.error(error);
    }
  }
</script>

<div class="flex flex-col items-center h-screen bg-white dark:bg-zinc-900">

  <h1 class="text-center text-3xl font-bold p-6 text-black dark:text-white">
    Edutain
  </h1>

  <h2 class="p-3 text-2xl font-bold text-black dark:text-white">Welcome</h2>
  <p class="text-lg w-3/4 text-center text-black dark:text-white">Edutain is a platform that allows you to learn *with the power of AI*.</p>
  <div class="p-3"></div>
  <div class="p-6">
    {#if $user}
      <div class="flex flex-row justify-center space-x-8 sm:space-x-16">
        <a href="/create-lesson">
          <button class='font-bold rounded-md text-white p-4 bg-green-600'>Enter Topic</button>
        </a>
        <button class="p-4 bg-red-500 text-white rounded-lg " on:click={() => signOut(auth)}>Sign out</button>
      </div>
    {:else}
      <a on:click={signInWithGoogle} href="/login">
        <button class='font-bold rounded-md text-white p-4 bg-blue-600'>Sign in with Google</button>
      </a>
    {/if}
  </div>
</div>
