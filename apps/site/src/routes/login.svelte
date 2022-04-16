<script lang="ts">
  import { goto } from '$app/navigation';
  import { AUTH_TOKEN_KEY } from '$lib/constants';
  import {
    Button,
    Form,
    InlineNotification,
    TextInput,
  } from 'carbon-components-svelte';
  import { httpService } from '../lib/http';

  let email = '';
  let password = '';
  let isLoading = false;
  let isErrored = false;
</script>

<Form
  class="m-auto space-y-8 text-left w-2/3 md:w-1/3"
  on:submit={async (e) => {
    e.preventDefault();
    isLoading = true;
    isErrored = false;
    const { data } = await httpService.post(`/user/login/`, {
      email: email,
      password: password,
    });
    if (!data.logged_in) isErrored = true;
    else {
      localStorage.setItem(AUTH_TOKEN_KEY, data.token);
      goto('/');
    }
    isLoading = false;
  }}
>
  <h1 class="font-bold text-5xl underline">Authorize</h1>
  <TextInput bind:value={email} required labelText="Email" />
  <TextInput
    bind:value={password}
    type="password"
    required
    labelText="Password"
  />
  {#if isErrored}
    <InlineNotification subtitle="The credentials you entered were wrong" />
  {/if}
  <Button type="submit" kind="primary" skeleton={isLoading}>
    Validate token
  </Button>
</Form>
