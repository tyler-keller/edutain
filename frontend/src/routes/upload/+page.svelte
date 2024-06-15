<script>
    import { auth, user } from '$lib/firebase';
    import { onMount } from 'svelte';

    let topic = '';
    let topicSubmission = false;
    let userStatus;

    $: topicIsValid = topic.length > 0 && topic.length < 32 && topic.trim() !== '';
    $: topicIsTouched = topic.length > 0;
    $: topicIsTooLong = topic.length > 32;

    onMount(() => {
        const unsubscribe = user.subscribe(value => {
            userStatus = value;
        });

        return () => unsubscribe();
    });

    const createLesson = () => {
        if (topic.trim() === '') {
            alert('Please enter a topic.');
            return;
        }

        // Add logic to handle lesson creation, e.g., saving to a database
        topicSubmission = true;
        console.log('Lesson created with topic:', topic);
    }

    const handleKeyDown = (event) => {
        if (event.key === 'Enter') {
            createLesson();
        }
    };
</script>

<div class="flex flex-col items-center h-screen bg-white dark:bg-zinc-900">
    <h1 class="text-black dark:text-white text-2xl text-center p-6 font-bold">Upload EPUB</h1>

    {#if $user}
        <div class="flex flex-col items-center h-screen">
            {#if topicSubmission}
                <p class="text-xl text-black dark:text-white">Lesson being created with topic: <strong>{topic}</strong></p>
                <div class="basis-1/4"></div>
            {:else}
                <div class="basis-1/4"></div>
            {/if}
            <div class="p-4 rounded-md dark:bg-zinc-600 bg-slate-200">
                <button 
                    class="p-2 m-2 bg-green-500 text-white rounded-md hover:bg-green-600"
                    on:click={createLesson}
                >
                    +
                </button>
                {#if topicIsTooLong}
                    <p class="text-red-500 dark:text-red-400">Topic must be less than 32 characters.</p>
                {/if}
            </div>
        </div>
    {:else}
        <p class="text-black dark:text-white">You need to be signed in to create a lesson.</p>
    {/if}
</div>

<style>
    /* Add any additional styles if necessary */
</style>
