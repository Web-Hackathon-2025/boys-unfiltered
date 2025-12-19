export const  queryKeys = {
  // Auth
  auth: {
    profile: ['auth', 'profile'],
  },
  
  // Users
  users: {
    all: ['users'],
    lists: () => [...queryKeys.users.all, 'list'],
    list: (filters) => [...queryKeys.users.lists(), { filters }],
    details: () => [...queryKeys.users.all, 'detail'],
    detail: (id) => [...queryKeys.users.details(), id],
  },
  
  // Services
  services: {
    all: ['services'],
    lists: () => [...queryKeys.services.all, 'list'],
    list: (filters) => [...queryKeys.services.lists(), { filters }],
    details: () => [...queryKeys.services.all, 'detail'],
    detail: (id) => [...queryKeys.services.details(), id],
    categories: ['services', 'categories'],
    packages: ['services', 'packages'],
    requests: {
      all: ['service-requests'],
      lists: () => [...queryKeys.services.requests.all, 'list'],
      list: (filters) => [...queryKeys.services.requests.lists(), { filters }],
      details: () => [...queryKeys.services.requests.all, 'detail'],
      detail: (id) => [...queryKeys.services.requests.details(), id],
    },
  },
  
  // Providers
  providers: {
    all: ['providers'],
    lists: () => [...queryKeys.providers.all, 'list'],
    list: (filters) => [...queryKeys.providers.lists(), { filters }],
    details: () => [...queryKeys.providers.all, 'detail'],
    detail: (id) => [...queryKeys.providers.details(), id],
    top: ['providers', 'top'],
    profile: ['providers', 'profile'],
    services: ['providers', 'services'],
    documents: ['providers', 'documents'],
    availability: ['providers', 'availability'],
    stats: ['providers', 'stats'],
  },
  
  // Bookings
  bookings: {
    all: ['bookings'],
    lists: () => [...queryKeys.bookings.all, 'list'],
    list: (filters) => [...queryKeys.bookings.lists(), { filters }],
    details: () => [...queryKeys.bookings.all, 'detail'],
    detail: (id) => [...queryKeys.bookings.details(), id],
    customer: ['bookings', 'customer'],
    provider: ['bookings', 'provider'],
    upcoming: ['bookings', 'upcoming'],
    stats: ['bookings', 'stats'],
    attachments: (id) => [...queryKeys.bookings.details(), id, 'attachments'],
  },
  
  // Payments
  payments: {
    all: ['payments'],
    lists: () => [...queryKeys.payments.all, 'list'],
    list: (filters) => [...queryKeys.payments.lists(), { filters }],
    details: () => [...queryKeys.payments.all, 'detail'],
    detail: (id) => [...queryKeys.payments.details(), id],
    wallet: ['payments', 'wallet'],
    transactions: ['payments', 'transactions'],
    stats: ['payments', 'stats'],
    refunds: {
      all: ['refunds'],
      details: () => [...queryKeys.payments.refunds.all, 'detail'],
      detail: (id) => [...queryKeys.payments.refunds.details(), id],
    },
  },
  
  // Reviews
  reviews: {
    all: ['reviews'],
    lists: () => [...queryKeys.reviews.all, 'list'],
    list: (filters) => [...queryKeys.reviews.lists(), { filters }],
    details: () => [...queryKeys.reviews.all, 'detail'],
    detail: (id) => [...queryKeys.reviews.details(), id],
    provider: (id) => ['reviews', 'provider', id],
    topRated: ['reviews', 'top-rated'],
    reports: {
      all: ['reports'],
      lists: () => [...queryKeys.reviews.reports.all, 'list'],
      details: () => [...queryKeys.reviews.reports.all, 'detail'],
      detail: (id) => [...queryKeys.reviews.reports.details(), id],
    },
  },
  
  // Notifications
  notifications: {
    all: ['notifications'],
    lists: () => [...queryKeys.notifications.all, 'list'],
    list: (filters) => [...queryKeys.notifications.lists(), { filters }],
    details: () => [...queryKeys.notifications.all, 'detail'],
    detail: (id) => [...queryKeys.notifications.details(), id],
    count: ['notifications', 'count'],
    preferences: ['notifications', 'preferences'],
  },
};