<script>
  import { auth, user } from '$lib/firebase';
  import { GoogleAuthProvider, signInWithPopup, signOut } from 'firebase/auth';
  import { navigate } from 'svelte-routing';
  import { onMount } from 'svelte';

  let files;
  let processing = false;

  async function signInWithGoogle() {
    const provider = new GoogleAuthProvider();
    try {
      const result = await signInWithPopup(auth, provider);
      console.log(result);
    } catch (error) {
      console.error(error);
    }
  }

  async function upload(e) {
    processing = true;
    const file = e.target.files[0];
    const formData = new FormData();
    formData.append('file', file);
    try {
      const response = await fetch('http://127.0.0.1:5000/upload', {
        method: 'POST',
        body: formData
      });
      if (response.ok) {
        // Redirect to the progress page
        navigate('/upload');
      } else {
        console.error('Failed to upload file:', response.statusText);
      }
    } catch (error) {
      console.error('Error uploading file:', error);
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
  <input accept=".epub" on:change={upload} bind:files type="file" id="book" name="book" class='hidden'>
  <div class="p-6">
    {#if $user}
      <div class="flex flex-row justify-center space-x-8 sm:space-x-16">
        <label for="book" class="font-bold rounded-md text-white p-4 bg-green-600 cursor-pointer">
          Upload EPUB
        </label>
        <button class="font-bold p-4 bg-red-500 text-white rounded-lg" on:click={() => signOut(auth)}>Sign out of {$user.displayName}</button>
      </div>
      {#if processing}
        <div class="flex flex-col items-center p-6">
          <p class="text-lg font-bold text-black dark:text-white">Processing...</p>
        </div>
      {/if}
    {:else}
      <a on:click={signInWithGoogle} href="/">
        <button class='font-bold rounded-md text-white p-4 bg-blue-600'>Sign in with Google</button>
      </a>
    {/if}
  </div>
</div>