interface Equipment {
    id?: number;
    name: string;
    type: string;
    total_quantity: number;
    available_quantity: number;
    description?: string;
    status?: string;
    price?: number;
    purchase_date?: string;
    location?: string;
}

interface Rental {
    id?: number;
    equipment_id: number;
    user_id: number;
    rental_quantity: number;
    rental_date?: string;
    expected_return_date: string;
    actual_return_date?: string;
    rental_status: number;
    deposit: number;
    rental_fee: number;
}

export type {
    Equipment,
    Rental
}