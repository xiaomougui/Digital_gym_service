export default function (): string {
    if (!localStorage.getItem('client_id')) {
        localStorage.setItem('client_id', crypto.randomUUID());
    }
    return localStorage.getItem('client_id')!;
}