<script>
    /** @type {import('./$types').PageData} */
    export let data;
</script>

<main>
    <h1>Create Lesson</h1>
    <form>
        <label>
            Title
            <input type="text" name="title" required>
        </label>
        <label>
            Description
            <textarea name="description" required></textarea>
        </label>
        <button type="submit">Create</button>
    </form>
</main>