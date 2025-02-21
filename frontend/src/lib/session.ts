import { writable, type Writable } from 'svelte/store';

type User = {
 email?: string | null;
 displayName?: string | null;
 photoURL?: string | null;
 uid?: string | null;
 location: {
    streetName: string | null;
    city: string | null;
    state: string | null;
    zipCode: string | null;
 }
 yelp: string | null;
};

export type SessionState = {
 user: User | null;
 loading?: boolean;
 loggedIn?: boolean;
};

export const session = <Writable<SessionState>>writable();